import unittest
from types import SimpleNamespace
from typing import cast
from unittest.mock import AsyncMock, Mock, patch

import discord

from events.xp import XpCog
from level import XpRepository
from tests._database import set_up_database

def make_message(
    user_id: int = 123456789012345678,
    *,
    is_bot: bool = False,
    guild_id: int | None = 1,
) -> tuple[discord.Message, AsyncMock]:
    send = AsyncMock()
    message = Mock(
        spec=discord.Message,
        author=SimpleNamespace(
            id=user_id,
            bot=is_bot,
            mention=f"<@{user_id}>",
            display_name="Test User",
            display_avatar=SimpleNamespace(url="https://example.com/avatar.png"),
        ),
        guild=None if guild_id is None else SimpleNamespace(id=guild_id),
        channel=Mock(spec=discord.TextChannel, send=send),
    )
    return cast(discord.Message, message), send

class XpEventTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        super().setUp()
        set_up_database(self)
        self.cog = XpCog()
        self.clock = self.enterContext(patch("events.xp.monotonic", return_value=100.0))

    async def test_server_message_awards_ten_xp(self) -> None:
        message, send = make_message()

        await self.cog.on_message(message)

        self.assertEqual(XpRepository.get_user_xp(message.author.id), 10)
        send.assert_not_awaited()

    async def test_bot_and_direct_messages_do_not_award_xp_or_notify(self) -> None:
        for is_bot, guild_id in ((True, 1), (False, None)):
            with self.subTest(is_bot=is_bot, guild_id=guild_id):
                message, send = make_message(is_bot=is_bot, guild_id=guild_id)

                await self.cog.on_message(message)

                self.assertEqual(XpRepository.get_user_xp(message.author.id), 0)
                send.assert_not_awaited()

    async def test_xp_awards_require_five_seconds_since_last_award(self) -> None:
        message, _ = make_message()

        for timestamp, expected_xp in (
            (0.0, 10),
            (4.999, 10),
            (5.0, 20),
            (9.999, 20),
            (10.0, 30),
        ):
            with self.subTest(timestamp=timestamp):
                self.clock.return_value = timestamp
                await self.cog.on_message(message)
                self.assertEqual(XpRepository.get_user_xp(message.author.id), expected_xp)

    async def test_cooldowns_are_independent_per_user(self) -> None:
        first, _ = make_message()
        second, _ = make_message(user_id=first.author.id + 1)

        await self.cog.on_message(first)
        await self.cog.on_message(second)

        self.assertEqual(XpRepository.get_user_xp(first.author.id), 10)
        self.assertEqual(XpRepository.get_user_xp(second.author.id), 10)

    async def test_notification_is_sent_only_when_level_increases(self) -> None:
        message, send = make_message()
        XpRepository.add_xp(message.author.id, 80)

        self.clock.return_value = 0.0
        await self.cog.on_message(message)

        self.assertEqual(XpRepository.get_user_xp(message.author.id), 90)
        send.assert_not_awaited()

        self.clock.return_value = 5.0
        await self.cog.on_message(message)

        self.assertEqual(XpRepository.get_user_xp(message.author.id), 100)
        send.assert_awaited_once()
        assert send.await_args is not None
        embed = send.await_args.kwargs["embed"]
        self.assertIn(message.author.mention, embed.description)
        fields = {field.name: field.value for field in embed.fields}
        self.assertEqual(fields["レベル"], "**1 → 2**")
        self.assertEqual(fields["累計XP"], "**100** XP")
