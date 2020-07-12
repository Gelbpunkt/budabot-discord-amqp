from __future__ import annotations

from dataclasses import dataclass

import discord
import orjson


@dataclass
class AOMessage:
    sender: str
    endpoint: str
    message: str

    @classmethod
    async def from_json(cls, data: dict[str, str]) -> AOMessage:
        return cls(**orjson.loads(data))

    async def send_to_discord(self, channel: discord.Channel):
        pass
