import asyncio
import logging

from types import ModuleType
from typing import Optional

import aio_pika
import discord

from .models import AOMessage
from .utils import chunks, format_amqp_message, format_discord_message


class RelayClient(discord.AutoShardedClient):
    """A discord Client instance"""

    def __init__(self, *args, **kwargs) -> None:
        self.config: ModuleType = kwargs.pop("config")
        self.discord_channel: Optional[discord.Channel] = None
        self.first_ready = True
        self.amqp_task: Optional[asyncio.Task] = None
        super().__init__(*args, **kwargs)

    async def close(self, *args, **kwargs) -> None:
        self.amqp_task.cancel()
        await self.amqp.close()
        await super().close(*args, **kwargs)

    async def connect_amqp(self) -> None:
        """Connects to the AMQP queue"""
        self.amqp = await aio_pika.connect_robust(self.config.amqp_uri)
        self.amqp_channel = await self.amqp.channel()
        self.amqp_queue = await self.amqp_channel.declare_queue(
            self.config.queue_name, auto_delete=True
        )
        self.amqp_exchange = await self.amqp_channel.declare_exchange(
            self.config.exchange_name, type="fanout", auto_delete=True
        )
        await self.amqp_queue.bind(self.amqp_exchange)

    async def amqp_consumer(self) -> None:
        await self.connect_amqp()
        """Listens for AMQP incoming messages and publishes to Discord"""
        async with self.amqp_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    if message.routing_key != self.config.queue_name:
                        logging.info(f"[AMQP Incoming] {message.body}")
                        message = AOMessage.from_json(message.body)
                        if self.discord_channel is not None:
                            text, embeds = format_amqp_message(
                                message, self.discord_channel.guild
                            )
                            await self.publish_discord(text, embeds)

    async def publish_amqp(self, text: str) -> None:
        """Helper function to publish something to AMQP"""
        await self.amqp_exchange.publish(
            aio_pika.Message(body=text.encode()), routing_key=self.config.queue_name,
        )

    async def publish_discord(self, text: str, embeds: list[tuple[str, str]]) -> None:
        """Helper function to publish something to Discord"""
        embeds = [
            discord.Embed(title=title, description=desc) for title, desc in embeds
        ]
        if len(text) <= 2000:
            await self.discord_channel.send(text, embed=embeds[0] if embeds else None)
        else:
            for idx, chunk in enumerate(chunks(text, 2000)):
                await self.discord_channel.send(
                    chunk, embed=embeds[idx] if len(embeds) > idx else None
                )

    async def on_ready(self) -> None:
        """
        Event fired when the bot is done connecting to Discord
        Used to load the channel to send to
        """
        logging.info("Client is ready")
        if self.first_ready:
            self.amqp_task = asyncio.create_task(self.amqp_consumer())
            self.discord_channel = self.get_channel(self.config.discord_channel_id)
            self.first_ready = False

    async def on_message(self, message: discord.Message) -> None:
        """
        Event fired when a message is sent on Discord
        """
        # Simple command handling
        # without commands.Bot as it has a lot of overhead
        confirm_command = f"{self.config.prefix}confirm "
        create_emoji_command = f"{self.config.prefix}createemojis"
        if message.content.startswith(confirm_command):
            content = message.content[len(confirm_command) :]
            await self.publish_amqp(f"discordconfirm {message.author.id} {content}")
            await message.channel.send(
                "I have submitted your discord confirmation request."
            )
        elif message.content.startswith(create_emoji_command):
            for emoji_file, emoji_name in self.config.emojis.items():
                with open(f"img/transparent_images/{emoji_file}", "rb") as fi:
                    data = fi.read()
                try:
                    await message.guild.create_custom_emoji(
                        name=emoji_name, image=data, reason="createemoji command"
                    )
                except discord.Forbidden:
                    return await message.channel.send(
                        "I seem to lack permissions to create emojis."
                    )
            await message.channel.send("Done creating emojis.")
        else:
            # Skip everything not in the relay channel or sent by the bot itself
            if (
                message.channel.id != self.config.discord_channel_id
                or message.author.bot
            ):
                return
            text = format_discord_message(message)
            logging.info(f"[Discord Incoming] {text}")
            await self.publish_amqp(text)
