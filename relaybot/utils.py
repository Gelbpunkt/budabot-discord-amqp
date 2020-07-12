import re

from typing import Any, Iterable, Iterator, List, Tuple

import discord

import config


def chunks(iterable: Iterable[Any], size: int) -> Iterator[Any]:
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


# A lot of helper regexes
# -----------------------
# Matches ingame image files
tdb_regex = re.compile(r"<img src=tdb://id:([A-Z|_|0-9]*)>")
# Matches any HTML element or entity
html_regex = re.compile(r"<[^:].*?>|\">|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
# Matches itemref:// links
itemref_regex = re.compile(
    r"<a href=(['\"])itemref://([0-9]+)/([0-9]+)/([0-9]+)\1>([A-z| |0-9]*)</a>"
)
# Matches itemid:// links to nanos
nano_regex = re.compile(r"<a href=(['\"])itemid://53019/([0-9]+)\1>([A-z| |0-9]*)</a>")
# Matches single-line img elements
img_regex = re.compile(r"^<img.+?>$\n", flags=re.MULTILINE | re.DOTALL)
# Matches clickable text
click_regex = re.compile(
    r"<a href=(['\"])text://(.+?)\1>(.*)</a>", flags=re.MULTILINE | re.DOTALL
)

# Helper replace functions
# ------------------------


def repl_emoji(text, emojis):
    def repl(match):
        actual = match.group(1)
        name = f"{actual}.png"
        if val := config.emojis.get(name):
            return str(discord.utils.get(emojis, name=val))
        else:
            return actual

    return re.sub(tdb_regex, repl, text)


def repl_itemref(text):
    return re.sub(
        itemref_regex,
        lambda m: f"[{discord.utils.escape_markdown(m.group(5))}](https://aoitems.com/item/{m.group(2)}/{m.group(4)}/)",
        text,
    )


def repl_nano(text):
    return re.sub(
        nano_regex,
        lambda m: f"[{discord.utils.escape_markdown(m.group(3))}](https://aoitems.com/item/{m.group(2)}/)",
        text,
    )


def repl_img(text):
    return re.sub(img_regex, "", text)


def repl_html(text):
    return re.sub(html_regex, "", text)


def format_amqp_message(
    message: str, guild: discord.Guild
) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Formats an AMQP message to publish to Discord.
    Returns a tuple of the message content and a list of strings for embed contents
    """
    # remove grc prefix
    message = message[4:]
    text = repl_emoji(message, guild.emojis)
    text = repl_img(text)

    # Find any clickable stuff
    embeds = []
    for match in re.finditer(click_regex, text):
        full = match.group(0)
        description = repl_itemref(match.group(2))
        description = repl_nano(description)
        description = repl_html(description)
        title = match.group(3)
        idx = text.index(full)
        text = text[:idx] + text[idx + len(full) :]
        if description.startswith(title):
            description = description[len(title) :]
        embeds.append((title, description))

    # Remove all HTML tags and entities from text
    text = repl_html(text)
    return text, embeds
