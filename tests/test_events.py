# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import uuid
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import AsyncMock
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID

import pytest

from manager_terminator.autogenerated_graphql_client.get_employee_managers import (
    GetEmployeeManagersManagers,
)
from manager_terminator.autogenerated_graphql_client.get_employee_managers import (
    GetEmployeeManagersManagersObjects,
)
from manager_terminator.autogenerated_graphql_client.get_engagement_objects_by_uuid import (
    GetEngagementObjectsByUuidEngagements,
)
from manager_terminator.autogenerated_graphql_client.get_engagement_objects_by_uuid import (
    GetEngagementObjectsByUuidEngagementsObjects,
)
from manager_terminator.autogenerated_graphql_client.terminate_manager import (
    TerminateManagerManagerTerminate,
)
from manager_terminator.helper_functions import (
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit,
)
from manager_terminator.main import engagement_event_handler
from manager_terminator.process_events import process_engagement_events
from manager_terminator.utils import DEFAULT_TIMEZONE
from tests.test_data import EMPLOYEE_OBJECTS
from tests.test_data import ENGAGEMENT_OBJECTS
from tests.test_data import (
    ENGAGEMENT_OBJECTS_MANAGER_AND_ENGAGEMENT_NOT_IN_SAME_ORG_UNIT,
)
from tests.test_data import (
    ENGAGEMENT_OBJECTS_MANAGER_WITH_EARLIER_END_DATE_THAN_ENGAGEMENT_END_DATE,
)
from tests.test_data import ENGAGEMENT_OBJECTS_NO_END_DATE_IN_ENGAGEMENT
from tests.test_data import ENGAGEMENT_OBJECTS_PERSON_IS_NOT_MANAGER
from tests.test_data import ENGAGEMENT_ORG_UNIT_OBJECTS
from tests.test_data import NO_ENGAGEMENT_OBJECTS_FOUND


@pytest.mark.asyncio
async def test_engagement_event_handler():
    """Tests the engagement_event_handler."""

    # test data
    test_data_engagement_uuid = uuid.uuid4()
    shared_orgunit_uuid = uuid.uuid4()
    shared_person_uuid = uuid.uuid4()

    test_data_engagement_objs = [
        {
            "uuid": test_data_engagement_uuid,
            "org_unit": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "person": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": test_data_engagement_uuid,
            "org_unit": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "person": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "validity": {
                "from": datetime(2023, 2, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": test_data_engagement_uuid,
            "org_unit": [{"uuid": shared_orgunit_uuid}],
            "person": [{"uuid": shared_person_uuid}],
            "validity": {
                "from": datetime(2023, 2, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": test_data_engagement_uuid,
            "org_unit": [{"uuid": shared_orgunit_uuid}],
            "person": [{"uuid": shared_person_uuid}],
            "validity": {
                "from": datetime(2023, 2, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": test_data_engagement_uuid,
            "org_unit": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "person": [
                {
                    "uuid": uuid.uuid4(),
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 2, 28, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
    ]

    test_data_managers = [
        {
            "uuid": uuid.uuid4(),
            "org_unit": [
                {
                    "uuid": test_data_engagement_objs[0]["org_unit"][0]["uuid"],
                }
            ],
            "person": [
                {
                    "uuid": test_data_engagement_objs[0]["person"][0]["uuid"],
                    "engagements": [test_data_engagement_objs[0]],
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": uuid.uuid4(),
            "org_unit": [
                {
                    "uuid": test_data_engagement_objs[1]["org_unit"][0]["uuid"],
                }
            ],
            "person": [
                {
                    "uuid": test_data_engagement_objs[1]["person"][0]["uuid"],
                    "engagements": [test_data_engagement_objs[1]],
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": uuid.uuid4(),
            "org_unit": [
                {
                    "uuid": test_data_engagement_objs[4]["org_unit"][0]["uuid"],
                }
            ],
            "person": [
                {
                    "uuid": test_data_engagement_objs[4]["person"][0]["uuid"],
                    "engagements": [test_data_engagement_objs[4]],
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
    ]

    # mocking
    get_engagement_objects_by_uuids_mock = AsyncMock(
        return_value=GetEngagementObjectsByUuidEngagements(
            objects=[
                GetEngagementObjectsByUuidEngagementsObjects(
                    objects=test_data_engagement_objs
                )
            ]
        )
    )

    get_employee_managers_mock = AsyncMock(
        return_value=GetEmployeeManagersManagers(
            objects=[GetEmployeeManagersManagersObjects(objects=test_data_managers)]
        )
    )

    terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data_managers[1]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_engagement_objects_by_uuids=get_engagement_objects_by_uuids_mock,
        get_employee_managers=get_employee_managers_mock,
        terminate_manager=terminate_manager_mock,
    )

    # invoke
    await engagement_event_handler(mo_mock, test_data_engagement_uuid, None)

    # asserts
    get_engagement_objects_by_uuids_mock.assert_called_once()
    get_employee_managers_mock.assert_has_calls(
        [
            call(
                # OBS: We convert a set to a list, since this is how the logic does it
                # and if we just use an array directly, the array passed to the
                # function, will be sorted, which will make the test fail.
                list(
                    {
                        test_data_engagement_objs[0]["person"][0]["uuid"],
                        test_data_engagement_objs[1]["person"][0]["uuid"],
                        test_data_engagement_objs[2]["person"][0]["uuid"],
                        test_data_engagement_objs[4]["person"][0]["uuid"],
                    }
                )
            )
        ]
    )
    terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data_managers[1]["uuid"],
                terminate_from=date(2023, 1, 1),
                terminate_to=date(2023, 1, 31),
            ),
            call(
                uuid=test_data_managers[2]["uuid"],
                terminate_from=None,
                terminate_to=test_data_engagement_objs[4]["validity"]["to"].date(),
            ),
        ]
    )


@pytest.mark.asyncio
async def test_engagement_event_handler_complex_data():
    # test data
    test_data_root_engagement_uuid = uuid.uuid4()

    shared_org_unit_uuid = uuid.uuid4()
    shared_person_uuid_1 = uuid.uuid4()

    test_data_engagements = [
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": shared_org_unit_uuid}],
            "person": [{"uuid": shared_person_uuid_1}],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 9, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": shared_org_unit_uuid}],
            "person": [{"uuid": shared_person_uuid_1}],
            "validity": {
                "from": datetime(2023, 9, 25, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 9, 25, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": shared_org_unit_uuid}],
            "person": [{"uuid": shared_person_uuid_1}],
            "validity": {
                "from": datetime(2023, 9, 26, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 11, 17, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": shared_org_unit_uuid}],
            "person": [{"uuid": shared_person_uuid_1}],
            "validity": {
                "from": datetime(2023, 11, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
    ]

    test_data_managers = [
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": shared_org_unit_uuid}],
            "person": [
                {
                    "uuid": shared_person_uuid_1,
                    "engagements": test_data_engagements,
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
    ]

    # mocking
    get_engagement_objects_by_uuids_mock = AsyncMock(
        return_value=GetEngagementObjectsByUuidEngagements(
            objects=[
                GetEngagementObjectsByUuidEngagementsObjects(
                    # NOTE: This object is just used to get the person_uuid,
                    # which is used later on to fetch employee managers
                    objects=[
                        {
                            "uuid": uuid.uuid4(),
                            "org_unit": [{"uuid": shared_org_unit_uuid}],
                            "person": [{"uuid": shared_person_uuid_1}],
                            "validity": {
                                "from": datetime(2023, 1, 1, 0, 0, 0).replace(
                                    tzinfo=DEFAULT_TIMEZONE
                                ),
                                "to": None,
                            },
                        },
                    ]
                )
            ]
        )
    )

    get_employee_managers_mock = AsyncMock(
        return_value=GetEmployeeManagersManagers(
            objects=[GetEmployeeManagersManagersObjects(objects=test_data_managers)]
        )
    )

    terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data_managers[0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_engagement_objects_by_uuids=get_engagement_objects_by_uuids_mock,
        get_employee_managers=get_employee_managers_mock,
        terminate_manager=terminate_manager_mock,
    )

    # invoke
    await engagement_event_handler(mo_mock, test_data_root_engagement_uuid, None)

    # asserts
    get_engagement_objects_by_uuids_mock.assert_called_once()
    get_employee_managers_mock.assert_has_calls([call([shared_person_uuid_1])])
    terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data_managers[0]["uuid"],
                terminate_from=(
                    test_data_engagements[0]["validity"]["to"] + timedelta(days=1)
                ).date(),
                terminate_to=(
                    test_data_engagements[1]["validity"]["from"] - timedelta(days=1)
                ).date(),
            ),
        ]
    )


@pytest.mark.asyncio
async def test_engagement_event_handler_engagements_across_orgunits():
    # test data
    person_uuid_shared = uuid.uuid4()
    ou_uuid_1 = uuid.uuid4()
    ou_uuid_2 = uuid.uuid4()
    ou_uuid_3 = uuid.uuid4()

    test_data_engagements = [
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_1}],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 1, 15, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_2}],
            "validity": {
                "from": datetime(2023, 5, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_3}],
            "validity": {
                "from": datetime(2023, 4, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 7, 10, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_3}],
            "validity": {
                "from": datetime(2023, 9, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 12, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
    ]

    test_data_managers = [
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": ou_uuid_3}],
            "person": [
                {
                    "uuid": person_uuid_shared,
                    "engagements": test_data_engagements,
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
    ]

    test_data_event_engagement_uuid = uuid.uuid4()

    # mocking
    get_engagement_objects_by_uuids_mock = AsyncMock(
        return_value=GetEngagementObjectsByUuidEngagements(
            objects=[
                GetEngagementObjectsByUuidEngagementsObjects(
                    # NOTE: This object is just used to get the person_uuid,
                    # which is used later on to fetch employee managers
                    objects=[
                        {
                            "uuid": uuid.uuid4(),
                            "person": [{"uuid": person_uuid_shared}],
                            "org_unit": [{"uuid": ou_uuid_1}],
                            "validity": {
                                "from": datetime(2023, 1, 1, 0, 0, 0).replace(
                                    tzinfo=DEFAULT_TIMEZONE
                                ),
                                "to": None,
                            },
                        },
                    ]
                )
            ]
        )
    )

    get_employee_managers_mock = AsyncMock(
        return_value=GetEmployeeManagersManagers(
            objects=[GetEmployeeManagersManagersObjects(objects=test_data_managers)]
        )
    )

    terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data_managers[0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_engagement_objects_by_uuids=get_engagement_objects_by_uuids_mock,
        get_employee_managers=get_employee_managers_mock,
        terminate_manager=terminate_manager_mock,
    )

    # invoke
    await engagement_event_handler(mo_mock, test_data_event_engagement_uuid, None)

    # asserts
    get_engagement_objects_by_uuids_mock.assert_called_once()
    get_employee_managers_mock.assert_has_calls([call([person_uuid_shared])])
    terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data_managers[0]["uuid"],
                terminate_from=(
                    test_data_engagements[0]["validity"]["to"] + timedelta(days=1)
                ).date(),
                terminate_to=(
                    test_data_engagements[2]["validity"]["from"] - timedelta(days=1)
                ).date(),
            )
        ]
    )


@pytest.mark.asyncio
async def test_engagement_event_handler_engagements_across_orgunits_no_infinity():
    # test data
    person_uuid_shared = uuid.uuid4()
    ou_uuid_1 = uuid.uuid4()
    ou_uuid_2 = uuid.uuid4()
    ou_uuid_3 = uuid.uuid4()

    test_data_engagements = [
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_1}],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 2, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_2}],
            "validity": {
                "from": datetime(2023, 7, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 8, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_3}],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 5, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
        {
            "uuid": uuid.uuid4(),
            "person": [{"uuid": person_uuid_shared}],
            "org_unit": [{"uuid": ou_uuid_3}],
            "validity": {
                "from": datetime(2023, 9, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": datetime(2023, 11, 30, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
            },
        },
    ]

    test_data_managers = [
        {
            "uuid": uuid.uuid4(),
            "org_unit": [{"uuid": ou_uuid_1}],
            "person": [
                {
                    "uuid": person_uuid_shared,
                    "engagements": test_data_engagements,
                }
            ],
            "validity": {
                "from": datetime(2023, 1, 1, 0, 0, 0).replace(tzinfo=DEFAULT_TIMEZONE),
                "to": None,
            },
        },
    ]

    test_data_event_engagement_uuid = uuid.uuid4()

    # mocking
    get_engagement_objects_by_uuids_mock = AsyncMock(
        return_value=GetEngagementObjectsByUuidEngagements(
            objects=[
                GetEngagementObjectsByUuidEngagementsObjects(
                    # NOTE: This object is just used to get the person_uuid,
                    # which is used later on to fetch employee managers
                    objects=[
                        {
                            "uuid": uuid.uuid4(),
                            "person": [{"uuid": person_uuid_shared}],
                            "org_unit": [{"uuid": ou_uuid_1}],
                            "validity": {
                                "from": datetime(2023, 1, 1, 0, 0, 0).replace(
                                    tzinfo=DEFAULT_TIMEZONE
                                ),
                                "to": None,
                            },
                        },
                    ]
                )
            ]
        )
    )

    get_employee_managers_mock = AsyncMock(
        return_value=GetEmployeeManagersManagers(
            objects=[GetEmployeeManagersManagersObjects(objects=test_data_managers)]
        )
    )

    terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=test_data_managers[0]["uuid"]
        )
    )

    mo_mock = AsyncMock(
        get_engagement_objects_by_uuids=get_engagement_objects_by_uuids_mock,
        get_employee_managers=get_employee_managers_mock,
        terminate_manager=terminate_manager_mock,
    )

    # invoke
    await engagement_event_handler(mo_mock, test_data_event_engagement_uuid, None)

    # asserts
    get_engagement_objects_by_uuids_mock.assert_called_once()
    get_employee_managers_mock.assert_has_calls([call([person_uuid_shared])])
    terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data_managers[0]["uuid"],
                terminate_from=(
                    test_data_engagements[2]["validity"]["to"] + timedelta(days=1)
                ).date(),
                terminate_to=(
                    test_data_engagements[1]["validity"]["from"] - timedelta(days=1)
                ).date(),
            ),
            call(
                uuid=test_data_managers[0]["uuid"],
                terminate_from=(
                    test_data_engagements[1]["validity"]["to"] + timedelta(days=1)
                ).date(),
                terminate_to=(
                    test_data_engagements[3]["validity"]["from"] - timedelta(days=1)
                ).date(),
            ),
            call(
                uuid=test_data_managers[0]["uuid"],
                terminate_from=None,
                terminate_to=test_data_engagements[3]["validity"]["to"].date(),
            ),
        ]
    )


# OLD tests belows


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_events_when_no_objects_found_successfully(mock_event_logger):
    """
    Tests if the process events function exits successfully if no engagement objects was found.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = NO_ENGAGEMENT_OBJECTS_FOUND
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")
    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_event_logger.info.assert_any_call(
        "No engagement objects found - event might be a termination. End process."
    )
    mocked_mo_client.terminate_manager.assert_not_awaited()


@pytest.mark.asyncio
@patch("manager_terminator.process_events.get_latest_end_date_from_engagement_objects")
async def test_process_engagements_event_terminate_managers_successfully(
    mock_get_latest_end_date_from_engagement_objects: MagicMock,
):
    """
    Tests if the manager terminates successfully as part of the event.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = ENGAGEMENT_OBJECTS
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")
    manager_uuid = UUID("29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101")
    termination_date = (
        mock_get_latest_end_date_from_engagement_objects.return_value
    ) = datetime(
        2023,
        9,
        20,
        0,
        0,
        tzinfo=timezone(timedelta(seconds=7200)),
    )
    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)

    mocked_mo_client.terminate_manager.assert_awaited_once_with(
        termination_date, manager_uuid
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_employee_not_a_manager(mock_events_logger):
    """
    Tests if function ends when employee is not a manager.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_PERSON_IS_NOT_MANAGER
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_events_logger.info.assert_any_call(
        "The person is not a manager. Event exited."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_has_no_end_date(mock_events_logger):
    """
    Tests if function ends when no engagement end date has been found.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_NO_END_DATE_IN_ENGAGEMENT
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)

    mock_events_logger.info.assert_any_call(
        "No end dates found on the persons engagement(s). End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_returns_none_when_terminate_managers_not_successful(
    mock_events_logger,
):
    """
    Tests if the process_engagement_events returns None when termination does not succeed.

    Tests if logging message gets properly logged with correct error level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_MANAGER_WITH_EARLIER_END_DATE_THAN_ENGAGEMENT_END_DATE
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    mock_events_logger.info.assert_any_call(
        "Manager will be terminated before farthest engagement. End event."
    )


@pytest.mark.asyncio
@patch("manager_terminator.process_events.logger")
async def test_process_engagements_event_get_manager_uuid_if_eng_in_same_org_returns_none(
    mock_events_logger,
):
    """
    Tests if function returns None when manager and engagement is not in same org unit.

    Tests if logging message gets properly logged with correct log level.
    """
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_engagement_objects.return_value = (
        ENGAGEMENT_OBJECTS_MANAGER_AND_ENGAGEMENT_NOT_IN_SAME_ORG_UNIT
    )
    engagement_uuid = UUID("fa5e2af6-ae28-4b6b-8895-3b7d39f93d54")

    await process_engagement_events(mocked_mo_client, engagement_uuid=engagement_uuid)
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit(
        EMPLOYEE_OBJECTS, ENGAGEMENT_ORG_UNIT_OBJECTS
    )
    mock_events_logger.error.assert_any_call(
        "The manager role might not exist in the same org unit as the engagement being"
        "created/updated/terminated."
    )
