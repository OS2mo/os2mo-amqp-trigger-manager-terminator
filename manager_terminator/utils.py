# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from zoneinfo import ZoneInfo

from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsValiditiesPersonEngagementsValidity,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsValiditiesValidity,
)


DEFAULT_TIMEZONE = ZoneInfo("Europe/Copenhagen")
POSITIVE_INFINITY = datetime.datetime.max.replace(tzinfo=datetime.UTC)


def validity_timezone_aware(
    validity: GetManagersManagersObjectsValiditiesValidity
    | GetManagersManagersObjectsValiditiesPersonEngagementsValidity,
):
    return {
        "from": validity["from"].replace(tzinfo=DEFAULT_TIMEZONE),
        "to": validity["to"].replace(tzinfo=DEFAULT_TIMEZONE)
        if validity["to"]
        else None,
    }
