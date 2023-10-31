# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from uuid import UUID

from manager_terminator.autogenerated_graphql_client.get_engagement_objects_by_uuid import (
    GetEngagementObjectsByUuidEngagementsObjects,
)
from manager_terminator.depends import GraphQLClient


async def get_by_uuid(
    mo: GraphQLClient, engagement_uuid: UUID
) -> list[GetEngagementObjectsByUuidEngagementsObjects]:
    resp_engagement_objs = await mo.get_engagement_objects_by_uuids([engagement_uuid])
    return [
        obj
        for wrapper_obj in resp_engagement_objs.objects
        for obj in wrapper_obj.objects
    ]
