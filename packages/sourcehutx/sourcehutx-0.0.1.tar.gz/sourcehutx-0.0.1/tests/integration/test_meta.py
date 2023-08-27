# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import pytest

from sourcehut.client import SrhtClient
from sourcehut.services import meta

from .. import vcr
from ..unit.test_meta import SSH_KEY_FINGERPRINT, SSH_KEY_KEY


@pytest.mark.asyncio
@vcr.use_cassette
async def test_meta_ssh_key(authed_client: SrhtClient):
    pub, fingerprint = SSH_KEY_KEY, SSH_KEY_FINGERPRINT
    async with authed_client:
        client = meta.MetaSrhtClient(authed_client)
        key = await client.create_ssh_key(pub)
        try:
            expected = meta.SSHKey(
                client=client,
                id=key.id,
                user=key.user,
                fingerprint=fingerprint,
                created=key.created,
                lastUsed=key.last_used,
                key=pub,
                comment="python-sourcehut tests",
            )
            assert key == expected
        finally:
            await key.delete()


@pytest.mark.asyncio
@vcr.use_cassette
async def test_meta_get_user_ref(authed_client: SrhtClient):
    async with authed_client:
        client = meta.MetaSrhtClient(authed_client)
        user_ref = await client.get_user_ref("gotmax23-test")
        expected = meta.UserRef(
            client=client,
            id=user_ref.id,
            username="gotmax23-test",
            email="maxwell+client-test@gtmx.me",
            canonicalName="~gotmax23-test",
        )
        assert user_ref == expected

        user_ref2 = await client.get_user_ref(user_ref)
        assert user_ref2 == expected


@pytest.mark.asyncio
@vcr.use_cassette
async def test_meta_get_user(authed_client: SrhtClient):
    bio = "Account for <https://git.sr.ht/~gotmax23/sourcehut>'s integration tests"
    async with authed_client:
        client = meta.MetaSrhtClient(authed_client)
        user = await client.get_user("gotmax23-test")
        expected = meta.User(
            client=client,
            id=user.id,
            username="gotmax23-test",
            email="maxwell+client-test@gtmx.me",
            canonicalName="~gotmax23-test",
            bio=bio,
            created=user.created,
            updated=user.updated,
            url=None,
            location=None,
        )
        assert user == expected

        user2 = await user.get()
        assert user2 == expected
