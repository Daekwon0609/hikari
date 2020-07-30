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
"""Events that fire when channels are modified.

This does not include message events, nor reaction events.
"""

from __future__ import annotations

__all__: typing.Final[typing.List[str]] = [
    "ChannelEvent",
    "GuildChannelEvent",
    "PrivateChannelEvent",
    "ChannelCreateEvent",
    "GuildChannelCreateEvent",
    "PrivateChannelCreateEvent",
    "ChannelUpdateEvent",
    "GuildChannelUpdateEvent",
    "PrivateChannelUpdateEvent",
    "ChannelDeleteEvent",
    "GuildChannelDeleteEvent",
    "PrivateChannelDeleteEvent",
    "ChannelPinsUpdateEvent",
    "GuildChannelPinsUpdateEvent",
    "PrivateChannelPinsUpdateEvent",
    "InviteCreateEvent",
    "InviteDeleteEvent",
    "WebhookUpdateEvent",
]

import abc
import typing

import attr

from hikari.events import base_events
from hikari.events import shard_events
from hikari.models import intents

if typing.TYPE_CHECKING:
    import datetime

    from hikari.api import shard as gateway_shard
    from hikari.models import channels
    from hikari.models import invites
    from hikari.utilities import snowflake


@base_events.requires_intents(
    intents.Intent.GUILDS, intents.Intent.PRIVATE_MESSAGES,
)
@attr.s(kw_only=True, slots=True)
class ChannelEvent(shard_events.ShardEvent, abc.ABC):
    """Event base for any channel-bound event in guilds or private messages."""

    @property
    @abc.abstractmethod
    def channel_id(self) -> snowflake.Snowflake:
        """ID of the channel the event relates to.

        Returns
        -------
        hikari.utilities.snowflake.Snowflake
            The ID of the channel this event relates to.
        """


@base_events.requires_intents(intents.Intent.GUILDS)
@attr.s(kw_only=True, slots=True)
class GuildChannelEvent(ChannelEvent, abc.ABC):
    """Event base for any channel-bound event in guilds."""

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
class PrivateChannelEvent(ChannelEvent, abc.ABC):
    """Event base for any channel-bound event in private messages."""


@base_events.requires_intents(intents.Intent.GUILDS, intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class ChannelCreateEvent(ChannelEvent, abc.ABC):
    """Base event for any channel being created."""

    @property
    @abc.abstractmethod
    def channel(self) -> channels.PartialChannel:
        """Channel this event represents.

        Returns
        -------
        hikari.models.channels.PartialChannel
            The channel that was created.
        """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id


@base_events.requires_intents(intents.Intent.GUILDS)
@attr.s(kw_only=True, slots=True)
class GuildChannelCreateEvent(GuildChannelEvent, ChannelCreateEvent):
    """Event fired when a guild channel is created."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel: channels.GuildChannel = attr.ib(repr=True)
    """Guild channel that this event represents.

    Returns
    -------
    hikari.models.channels.GuildChannel
        The guild channel that was created.
    """

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildChannelEvent>>.
        return self.channel.guild_id


@base_events.requires_intents(intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class PrivateChannelCreateEvent(PrivateChannelEvent, ChannelCreateEvent):
    """Event fired when a private channel is created."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel: channels.PrivateChannel = attr.ib(repr=True)
    """Private channel that this event represents.

    Returns
    -------
    hikari.models.channels.PrivateChannel
        The guild channel that was created.
    """


@base_events.requires_intents(intents.Intent.GUILDS, intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class ChannelUpdateEvent(ChannelEvent, abc.ABC):
    """Base event for any channel being updated."""

    @property
    @abc.abstractmethod
    def channel(self) -> channels.PartialChannel:
        """Channel this event represents.

        Returns
        -------
        hikari.models.channels.PartialChannel
            The channel that was created.
        """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id


@base_events.requires_intents(intents.Intent.GUILDS)
@attr.s(kw_only=True, slots=True)
class GuildChannelUpdateEvent(GuildChannelEvent, ChannelUpdateEvent):
    """Event fired when a guild channel is edited."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel: channels.GuildChannel = attr.ib(repr=True)
    """Guild channel that this event represents.

    Returns
    -------
    hikari.models.channels.GuildChannel
        The guild channel that was updated.
    """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildChannelEvent>>.
        return self.channel.guild_id


@base_events.requires_intents(intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class PrivateChannelUpdateEvent(PrivateChannelEvent, ChannelUpdateEvent):
    """Event fired when a private channel is edited."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel: channels.PrivateChannel = attr.ib(repr=True)
    """Private channel that this event represents.

    Returns
    -------
    hikari.models.channels.PrivateChannel
        The private channel that was updated.
    """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id


@base_events.requires_intents(intents.Intent.GUILDS, intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class ChannelDeleteEvent(ChannelEvent, abc.ABC):
    """Base event for any channel being deleted."""

    @property
    @abc.abstractmethod
    def channel(self) -> channels.PartialChannel:
        """Channel this event represents.

        Returns
        -------
        hikari.models.channels.PartialChannel
            The channel that was created.
        """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id


@base_events.requires_intents(intents.Intent.GUILDS)
@attr.s(kw_only=True, slots=True)
class GuildChannelDeleteEvent(GuildChannelEvent, ChannelDeleteEvent):
    """Event fired when a guild channel is deleted."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel: channels.GuildChannel = attr.ib(repr=True)
    """Guild channel that this event represents.

    Returns
    -------
    hikari.models.channels.GuildChannel
        The guild channel that was deleted.
    """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildChannelEvent>>.
        return self.channel.guild_id


# TODO: can this actually ever get fired?
@base_events.requires_intents(intents.Intent.PRIVATE_MESSAGES)
@attr.s(kw_only=True, slots=True)
class PrivateChannelDeleteEvent(PrivateChannelEvent, ChannelDeleteEvent):
    """Event fired when a private channel is deleted."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring>>.

    channel: channels.PrivateChannel = attr.ib(repr=True)
    """Private channel that this event represents.

    Returns
    -------
    hikari.models.channels.PrivateChannel
        The private channel that was deleted.
    """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.channel.id


# TODO: find out what private message intents are needed.
@attr.s(kw_only=True, slots=True)
class ChannelPinsUpdateEvent(ChannelEvent, abc.ABC):
    """Base event fired when a message is pinned/unpinned in a channel."""

    @property
    @abc.abstractmethod
    def last_pin_timestamp(self) -> typing.Optional[datetime.datetime]:
        """Datetime of when the most recent message was pinned in the channel.

        Will be `builtins.None` if nothing is pinned or the information is
        unavailable.

        Returns
        -------
        datetime.datetime or builtins.None
            The datetime of the most recent pinned message in the channel,
            or `builtins.None` if no pins are available.
        """


@base_events.requires_intents(intents.Intent.GUILDS)
@attr.s(kw_only=True, slots=True)
class GuildChannelPinsUpdateEvent(ChannelPinsUpdateEvent, GuildChannelEvent):
    """Event fired when a message is pinned/unpinned in a guild channel."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from ChannelEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildChannelEvent>>.

    last_pin_timestamp: typing.Optional[datetime.datetime] = attr.ib(repr=True)
    # <<inherited docstring from ChannelPinsUpdateEvent>>.


# TODO: This isn't documented as having an intent, is this right? The guild version requires GUILDS intent.
@attr.s(kw_only=True, slots=True)
class PrivateChannelPinsUpdateEvent(ChannelPinsUpdateEvent, PrivateChannelEvent):
    """Event fired when a message is pinned/unpinned in a private channel."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from ChannelEvent>>.

    last_pin_timestamp: typing.Optional[datetime.datetime] = attr.ib(repr=True)
    # <<inherited docstring from ChannelPinsUpdateEvent>>.


@base_events.requires_intents(intents.Intent.GUILD_INVITES)
@attr.s(kw_only=True, slots=True)
class InviteEvent(GuildChannelEvent, abc.ABC):
    """Base event type for guild invite updates."""

    @property
    @abc.abstractmethod
    def code(self) -> str:
        """Code that is used in the URL for the invite.

        Returns
        -------
        builtins.str
            The invite code.
        """


@base_events.requires_intents(intents.Intent.GUILD_INVITES)
@attr.s(kw_only=True, slots=True)
class InviteCreateEvent(InviteEvent):
    """Event fired when an invite is created in a channel."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    invite: invites.Invite = attr.ib()
    """Invite that was created.

    Returns
    -------
    hikari.models.invites.Invite
        The created invite object.
    """

    @property
    def channel_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from ChannelEvent>>.
        return self.invite.channel_id

    @property
    def guild_id(self) -> snowflake.Snowflake:
        # <<inherited docstring from GuildChannelEvent>>.
        # This will always be non-None for guild channel invites.
        return typing.cast(snowflake.Snowflake, self.invite.guild_id)

    @property
    def code(self) -> str:
        # <<inherited docstring from InviteEvent>>.
        return self.invite.code


@base_events.requires_intents(intents.Intent.GUILD_INVITES)
@attr.s(kw_only=True, slots=True)
class InviteDeleteEvent(InviteEvent):
    """Event fired when an invite is deleted from a channel."""

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from ChannelEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildChannelEvent>>.

    code: str = attr.ib()
    # <<inherited docstring from InviteEvent>>.


@base_events.requires_intents(intents.Intent.GUILD_WEBHOOKS)
@attr.s(kw_only=True, slots=True)
class WebhookUpdateEvent(GuildChannelEvent):
    """Event fired when a webhook is created/updated/deleted in a channel.

    Unfortunately, Discord does not provide any information on what webhook
    actually changed, nor specifically whether it was created/updated/deleted,
    so this event is pretty useless unless you keep track of the webhooks in
    the channel manually beforehand.
    """

    shard: gateway_shard.IGatewayShard = attr.ib()
    # <<inherited docstring from ShardEvent>>.

    channel_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from ChannelEvent>>.

    guild_id: snowflake.Snowflake = attr.ib()
    # <<inherited docstring from GuildChannelEvent>>.