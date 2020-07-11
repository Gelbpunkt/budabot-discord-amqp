import re

import discord

import config


def chunks(iterable, size):
    """Yield successive n-sized chunks from an iterable."""
    for i in range(0, len(iterable), size):
        yield iterable[i : i + size]


def format_discord_message(message: discord.Message) -> str:
    """Formats a Discord message to publish to AMQP"""
    mapping = {
        "server": message.guild.name,
        "channel": message.channel.name,
        "nick": message.author.display_name,
        "username": message.author.name,
        "discrim": message.author.discriminator,
        "content": message.content,
    }
    msg = config.chat_format.format(**mapping)
    msg = f"grc {msg}"
    return msg


def format_amqp_message(message: str) -> str:
    """Formats an AMQP message to publish to Discord"""
    # remove grc prefix
    message = message[4:]
    html_regex = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    # Remove all HTML tags and entities from text
    text = re.sub(html_regex, "", message)
    return text
