# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019-2020
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""Events that fire when something occurs within a guild."""

from __future__ import annotations

__all__: typing.Final[typing.List[str]] = [
    "GuildVisibilityEvent",
    "GuildAvailableEvent",
    "GuildUnavailableEvent",
    "GuildLeaveEvent",
    "GuildUpdateEvent",
    "BanEvent",
    "BanCreateEvent",
    "BanDeleteEvent",
    "EmojisUpdateEvent",
    "IntegrationsUpdateEvent",
    "PresenceUpdateEvent",
]

import abc
import typing

import attr

from hikari.events import base_events
from hikari.events import shard_events
from hikari.models import intents

if typing.TYPE_CHECKING:
    from hikari.api import shard as gateway_shard
    from hikari.models import emojis as emojis_
    from hikari.models import guilds
    from hikari.models import presences
    from hikari.models import users
    from hikari.utilities import snowflake


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILDS)
class GuildVisibilityEvent(shard_events.ShardEvent, abc.ABC):
    """Event base for any event that changes the visibility of a guild.

    This includes when a guild becomes available after an outage, when a
    guild becomes available on startup, when a guild becomes unavailable due
    to an outage, when the user is kicked/banned/leaves a guild, or when
    the user joins a new guild.
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> snowflake.Snowflake:
        """ID of the guild that this event relates to.

        Returns
        -------
        hikari.utilities.snowflake.Snowflake
            The ID of the guild that relates to this event.
        """


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILDS)
class GuildAvailableEvent(GuildVisibilityEvent):
    """Event fired when a guild becomes available.

    This will occur on startup, after outages, and if the bot joins a new guild.
    """

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild: guilds.Guild = attr.ib()
    """Guild that just became available.

    Returns
    -------
    hikari.models.guilds.Guild
        The guild that relates to this event.
    """

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildEvent>>.
        return self.guild.id


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILDS)
class GuildLeaveEvent(GuildVisibilityEvent):
    """Event fired when the bot is banned/kicked/leaves a guild.

    This will also fire if the guild was deleted.
    """

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildEvent>>.


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILDS)
class GuildUnavailableEvent(GuildVisibilityEvent):
    """Event fired when a guild becomes unavailable because of an outage."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildEvent>>.


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILDS)
class GuildUpdateEvent(shard_events.ShardEvent):
    """Event fired when an existing guild is updated."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild: guilds.Guild = attr.ib()
    """Guild that was just updated.

    Returns
    -------
    hikari.models.guilds.Guild
        The guild that relates to this event.
    """

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildEvent>>.
        return self.guild.id


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_BANS)
class BanEvent(shard_events.ShardEvent, abc.ABC):
    """Event base for any guild ban or unban."""

    @property
    @abc.abstractmethod
    def guild_id(self) -> snowflake.Snowflake:
        """ID of the guild that this event relates to.

        Returns
        -------
        hikari.utilities.snowflake.Snowflake
            The ID of the guild that relates to this event.
        """

    @property
    @abc.abstractmethod
    def user(self) -> users.User:
        """User that this ban event affects.

        Returns
        -------
        hikari.models.users.User
            The user that this event concerns.
        """


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_BANS)
class BanCreateEvent(BanEvent):
    """Event that is fired when a user is banned from a guild."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildEvent>>.

    user: users.User = attr.ib()
    # <<inherited docstring from BanEvent>>.


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_BANS)
class BanDeleteEvent(BanEvent):
    """Event that is fired when a user is unbanned from a guild."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildEvent>>.

    user: users.User = attr.ib()
    # <<inherited docstring from BanEvent>>.


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_EMOJIS)
class EmojisUpdateEvent(shard_events.ShardEvent):
    """Event that is fired when the emojis in a guild are updated."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    """ID of the guild that this event relates to.

    Returns
    -------
    hikari.utilities.snowflake.Snowflake
        The ID of the guild that relates to this event.
    """

    emojis: typing.Sequence[emojis_.KnownCustomEmoji] = attr.ib()
    """Sequence of all emojis in this guild.

    Returns
    -------
    typing.Sequence[emojis_.KnownCustomEmoji]
        All emojis in the guild.
    """


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_EMOJIS)
class IntegrationsUpdateEvent(shard_events.ShardEvent):
    """Event that is fired when the integrations in a guild are changed.

    This may occur when integrations are created, updated, or deleted.

    !!! note
        This event is similar to
        `hikari.events.channel_events.WebhookUpdateEvent` in that Discord
        does not provide any information on what was actually changed, nor
        how it was changed. The only way you will be able to determine this is
        to keep a cache of this information manually up to date by fetching
        it using REST API calls. This is a limitation of Discord's design.
        We agree that it is not overly helpful to you.
    """

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    """ID of the guild that this event relates to.

    Returns
    -------
    hikari.utilities.snowflake.Snowflake
        The ID of the guild that relates to this event.
    """


@attr.s(kw_only=True, slots=True)
@base_events.requires_intents(intents.Intent.GUILD_PRESENCES)
class PresenceUpdateEvent(shard_events.ShardEvent):
    """Event fired when a user in a guild updates their presence in a guild.

    Sent when a guild member changes their presence in a specific guild.

    If the user is changed (e.g. new username), then this may fire many times
    (once for every guild the bot is part of). This is a limitation of how
    Discord implements their event system, unfortunately.

    Furthermore, if the target user is a bot and the bot only updates their
    presence on specific shards, this will only fire for the corresponding
    shards that saw the presence update.
    """

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    presence: presences.MemberPresence = attr.ib()
    """Member presence.

    Returns
    -------
    hikari.models.presences.MemberPresence
        Presence for the user in this guild.
    """

    user: typing.Optional[users.PartialUser] = attr.ib()
    """User that was updated.

    This is a partial user object that only contains the fields that were
    updated on the user profile.

    Will be `builtins.None` if the user itself did not change.
    This is always the case if the user only updated their member
    representation and did not change their user profile directly.

    Returns
    -------
    hikari.models.users.PartialUser or builtins.None
        The partial user containing the updated fields.
    """

    @property
    def user_id(self) -> snowflake.Snowflake:
        """User ID of the user that updated their presence.

        Returns
        -------
        hikari.utilities.snowflake.Snowflake
            ID of the user the event concerns.
        """
        return self.presence.user_id

    @property
    def guild_id(self) -> snowflake.Snowflake:
        """Guild ID that the presence was updated in.

        Returns
        -------
        hikari.utilities.snowflake.Snowflake
            ID of the guild the event occurred in.
        """
        # Should always be present in this event.
        return typing.cast("snowflake.Snowflake", self.presence.guild_id)