#!/bin/env python
import logging

import discord

import config

from relaybot.client import RelayClient

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

if __name__ == "__main__":
    client.start_all()
