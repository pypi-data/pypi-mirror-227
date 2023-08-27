# Copyright (C) 2023 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

from typing import Any

import pytest
import respx

from sourcehut.client import SrhtClient
from sourcehut.services import builds

JOB_DATA_1: dict[str, Any] = {
    "id": 1039160,
    "created": "2023-08-11T06:00:02.050859Z",
    "updated": "2023-08-11T06:03:50.753334Z",
    "status": "SUCCESS",
    "manifest": "",
    "note": "",
    "tags": ["fedora-scripts", "scheduled", "go-leaves"],
    "visibility": "PUBLIC",
    "image": "fedora/rawhide",
}


@pytest.mark.asyncio
async def test_builds_get_build(fake_client: SrhtClient):
    with respx.mock() as respx_mock:
        async with fake_client:
            client = builds.BuildsSrhtClient(fake_client)
            endpoint = client.client.get_endpoint(client.SERVICE)
            route = respx_mock.post(endpoint).respond(
                json={"data": {"job": JOB_DATA_1}}
            )
            gotten = await client.get_job(1039160)
            assert gotten == builds.Job(**JOB_DATA_1, client=client)
            assert route.call_count == 1
            second = await gotten.get()
            assert second == gotten
            assert route.call_count == 2
            status = await client.get_job_status(gotten)
            assert status.succeeded
            assert route.call_count == 3


def test_builds_job_status():
    pending = builds.JOB_STATUS.PENDING
    assert pending.in_progress
    assert not pending.succeeded
    assert not pending.failed
    assert str(pending) == "PENDING"

    assert builds.JOB_STATUS.SUCCESS.succeeded
    assert builds.JOB_STATUS.TIMEOUT.failed
