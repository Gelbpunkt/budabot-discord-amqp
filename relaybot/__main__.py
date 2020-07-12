#!/bin/env python
import logging
import sys

import orjson

# Ugly patch to use orjson globally
sys.modules["json"] = orjson
sys.path.insert(0, "/bot")

import discord
import uvloop

import config

from .client import RelayClient

# Set up a log handler
logging.basicConfig(
    filename=config.logfile, level=logging.INFO,
)

# discord.py client with all caching disabled as we don't need it
# the status will say "Playing Anarchy Online"
client = RelayClient(
    max_messages=None,
    fetch_offline_members=False,
    activity=discord.Game("Anarchy Online"),
    config=config,
)


def run():
    uvloop.install()
    client.run(config.token)


if __name__ == "__main__":
    run()
