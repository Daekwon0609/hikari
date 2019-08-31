#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
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
from unittest import mock

import pytest
import datetime

from hikari.core.model import invite
from hikari.core.model import model_cache


@pytest.mark.model
class TestInvite:
    def test_Invite_from_dict(self):
        test_state = mock.MagicMock(state_set=model_cache.AbstractModelCache)

        guild_dict = {"id": "165176875973476352", "name": "CS:GO Fraggers Only", "splash": None, "icon": None}
        channel_dict = {"id": "165176875973476352", "name": "illuminati", "type": 0}
        user_dict = {"id": "165176875973476352", "username": "bob", "avatar": "deadbeef", "discriminator": "#1234"}

        inv = invite.Invite.from_dict(
            test_state,
            {
                "code": "0vCdhLbwjZZTWZLD",
                "guild": guild_dict,
                "channel": channel_dict,
                "target_user": user_dict,
                "target_user_type": 1,
                "approximate_presence_count": 69,
                "approximate_member_count": 420,
            },
        )

        assert inv.code == "0vCdhLbwjZZTWZLD"
        assert inv.target_user_type == 1
        assert inv.approximate_presence_count == 69
        assert inv.approximate_member_count == 420
        test_state.parse_user.assert_called_with(user_dict)
        test_state.parse_guild.assert_called_with(guild_dict)
        test_state.parse_channel.assert_called_with(channel_dict)


@pytest.mark.model
class TestInviteMetadata:
    def test_InviteMetadata_from_dict(self):
        test_state = mock.MagicMock(state_set=model_cache.AbstractModelCache)

        user_dict = {
            "id": "80351110224678912",
            "username": "Nelly",
            "discriminator": "1337",
            "avatar": "8342729096ea3675442027381ff50dfe",
            "verified": True,
            "email": "nelly@discordapp.com",
            "flags": 64,
            "premium_type": 1,
        }

        invm = invite.InviteMetadata.from_dict(
            test_state,
            {
                "inviter": user_dict,
                "uses": 69,
                "max_uses": 420,
                "max_age": 99999,
                "temporary": True,
                "created_at": "2016-03-31T19:15:39.954000+00:00",
                "revoked": True,
            },
        )

        assert invm.uses == 69
        assert invm.max_uses == 420
        assert invm.max_age == 99999
        assert invm.temporary is True
        assert invm.revoked is True
        assert invm.created_at == datetime.datetime(2016, 3, 31, 19, 15, 39, 954000, tzinfo=datetime.timezone.utc)
        test_state.parse_user.assert_called_with(user_dict)