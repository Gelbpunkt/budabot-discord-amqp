import re

import discord


def format_discord_message(message: discord.Message) -> str:
    """Formats a Discord message to publish to AMQP"""
    msg = f"{message.author}: {message.content}"
    return msg


def format_amqp_message(message: str) -> str:
    """Formats an AMQP message to publish to Discord"""
    html_regex = re.compile(r"<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
    # Remove all HTML tags and entities from text
    text = re.sub(html_regex, "", message)
    return text
