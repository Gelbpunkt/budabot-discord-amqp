import asyncio
import logging
import signal

from types import ModuleType
from typing import Optional

import aio_pika
import discord

from .utils import format_amqp_message, format_discord_message


class RelayClient(discord.Client):
    """A discord Client instance"""

    def __init__(self, *args, **kwargs) -> None:
        self.config: ModuleType = kwargs.pop("config")
        self.discord_channel: Optional[discord.Channel] = None
        super().__init__(*args, **kwargs)

    def start_all(self) -> None:
        """Starts the AMQP and Discord listeners"""
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
        loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())

        async def runner() -> None:
            try:
                await self.start(self.config.token)
            finally:
                await self.close()

        def stop_loop_on_completion(_) -> None:
            loop.stop()

        fut = asyncio.ensure_future(runner(), loop=loop)
        fut.add_done_callback(stop_loop_on_completion)
        asyncio.ensure_future(self.amqp_consumer(), loop=loop)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logging.info("Received signal to terminate bot and event loop.")
        finally:
            fut.remove_done_callback(stop_loop_on_completion)

    async def connect_amqp(self) -> None:
        """Connects to the AMQP queue"""
        self.amqp = await aio_pika.connect_robust(self.config.amqp_uri)
        self.amqp_channel = await self.amqp.channel()
        self.amqp_queue = await self.amqp_channel.declare_queue(
            self.config.queue_name, auto_delete=True
        )
        self.amqp_exchange = await self.amqp_channel.declare_exchange(
            self.config.amqp_exchange, type="fanout", auto_delete=True
        )
        await self.amqp_queue.bind(self.amqp_exchange)

    async def amqp_consumer(self) -> None:
        await self.connect_amqp()
        """Listens for AMQP incoming messages and publishes to Discord"""
        async with self.amqp_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = message.body.decode()
                    if (
                        message.routing_key != self.config.queue_name
                        and body.startswith("grc ")
                    ):
                        logging.info(f"[AMQP Incoming] {body}")
                        text = format_amqp_message(body)
                        await self.publish_discord(text)

    async def publish_amqp(self, text: str) -> None:
        """Helper function to publish something to AMQP"""
        await self.amqp_exchange.publish(
            aio_pika.Message(body=text.encode()), routing_key=self.config.queue_name,
        )

    async def publish_discord(self, text: str) -> None:
        """Helper function to publish something to Discord"""
        if self.discord_channel is not None:
            await self.discord_channel.send(text)

    async def on_ready(self) -> None:
        """
        Event fired when the bot is done connecting to Discord
        Used to load the channel to send to
        """
        logging.info("Client is ready")
        self.discord_channel = self.get_channel(self.config.discord_channel_id)

    async def on_message(self, message: discord.Message) -> None:
        """
        Event fired when a message is sent on Discord
        """
        # Simple command handling
        # without commands.Bot as it has a lot of overhead
        confirm_command = f"{self.config.prefix}confirm "
        if message.content.startswith(confirm_command):
            content = message.content[len(confirm_command) :]
            await self.publish_amqp(f"discordconfirm {message.author.id} {content}")
            await message.channel.send(
                "I have submitted your discord confirmation request."
            )
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
