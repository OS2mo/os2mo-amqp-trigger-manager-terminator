# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from unittest.mock import AsyncMock
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

import httpx
import pytest
import respx
from httpx import Response

from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagers,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjects,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjects,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsEmployee,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsEmployeeEngagements,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsEmployeeEngagementsValidity,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsOrgUnit,
)
from manager_terminator.autogenerated_graphql_client.get_managers import (
    GetManagersManagersObjectsObjectsValidity,
)
from manager_terminator.autogenerated_graphql_client.terminate_manager import (
    TerminateManagerManagerTerminate,
)
from manager_terminator.main import initiate_terminator
from manager_terminator.terminate_managers_init.init_manager_terminator import (
    terminator_initialiser,
)
from manager_terminator.utils import validity_timezone_aware
from tests.test_data import MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS


@pytest.mark.asyncio
async def test_initiate_terminator():
    """
    Tests if the initiate_terminator functions terminator_initialiser
    is called as expected
    """
    # Mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers(objects=TEST_DATA_MANAGERS)
    )
    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=TEST_DATA_MANAGERS[0].objects[0].uuid
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # Invoke & assert
    await initiate_terminator(mo_mock)
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_has_calls(
        [
            # First manager
            call(
                uuid=TEST_DATA_MANAGERS[0].objects[0].uuid,
                terminate_from=datetime.date(2023, 3, 2),
                terminate_to=datetime.date(2023, 4, 30),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[0].objects[0].uuid,
                terminate_from=datetime.date(2023, 6, 2),
                terminate_to=datetime.date(2023, 9, 30),
            ),
            # Second manager
            call(
                uuid=TEST_DATA_MANAGERS[1].objects[0].uuid,
                terminate_from=datetime.date(2023, 1, 1),
                terminate_to=datetime.date(2023, 1, 31),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1].objects[0].uuid,
                terminate_from=datetime.date(2023, 5, 1),
                terminate_to=datetime.date(2023, 5, 31),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1].objects[0].uuid,
                terminate_from=datetime.date(2023, 9, 1),
                terminate_to=datetime.date(2023, 9, 30),
            ),
            call(
                uuid=TEST_DATA_MANAGERS[1].objects[0].uuid,
                terminate_from=datetime.date(2023, 12, 1),
                terminate_to=datetime.date(2023, 12, 31),
            ),
        ]
    )


@pytest.mark.asyncio
async def test_initiate_terminator_dry_run():
    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers(objects=TEST_DATA_MANAGERS)
    )

    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(
            uuid=TEST_DATA_MANAGERS[0].objects[0].uuid
        )
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock, dryrun=True)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_not_called()


@pytest.mark.asyncio
async def test_initiate_terminator_tailing_engagements():
    """Verifies a manager which engagements tail eachother.

    ex:
    - manger validity: 2023-05-15 -> infinity
    - engagement 1 validity: 2023-01-01 -> 2023-05-14
    - engagement 2 validity: 2023-05-15 -> 2023-07-31
    - engagement 3 validity: 2023-08-01 -> infinity

    this should not result in a termination of the manager.
    """

    test_data = [
        _create_test_data_manager_with_employee_engagements(
            manager_validity=GetManagersManagersObjectsObjectsValidity(
                from_=datetime.datetime(2023, 5, 15, 0, 0), to=None
            ),
            engagement_validities=[
                GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                    from_=datetime.datetime(2023, 1, 1, 0, 0),
                    to=datetime.datetime(2023, 5, 14, 0, 0),
                ),
                GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                    from_=datetime.datetime(2023, 5, 15, 0, 0),
                    to=datetime.datetime(2023, 7, 31, 0, 0),
                ),
                GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                    from_=datetime.datetime(2023, 8, 1, 0, 0),
                    to=None,
                ),
            ],
        ),
    ]

    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers(objects=test_data)
    )

    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(uuid=test_data[0].objects[0].uuid)
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_not_called()


@pytest.mark.asyncio
async def test_initiate_terminator_terminate_entire_infinity_manager():
    """Verfies a manager with no engagements and no end-date, is terminated correctly

    A manager with an end-date of infinity, is treated differently since our GraphQL
    termination-mutation does not accept infinity as a valid to-date.

    So instead we need to set from=None and to=manager_validity.from, which the
    mutator then treats as a termination of the entire manager from the
    manager_validity.from to infinity.

    NOTE: This is due to how the termination-mutators have been implemented.
    Ideally the mutator should be fixed so we can set to=None
    and then always require "from"-date instead of "to"-date.
    """

    test_data = [
        _create_test_data_manager_with_employee_engagements(
            manager_validity=GetManagersManagersObjectsObjectsValidity(
                from_=datetime.datetime(2023, 1, 1, 0, 0), to=None
            ),
            engagement_validities=[],
        ),
    ]

    # mocking
    mo_get_managers_mock = AsyncMock(
        return_value=GetManagersManagers(objects=test_data)
    )

    mo_terminate_manager_mock = AsyncMock(
        return_value=TerminateManagerManagerTerminate(uuid=test_data[0].objects[0].uuid)
    )

    mo_mock = AsyncMock(
        get_managers=mo_get_managers_mock,
        terminate_manager=mo_terminate_manager_mock,
    )

    # invoke
    await initiate_terminator(mo_mock)

    # asserts
    mo_get_managers_mock.assert_called_once()
    mo_terminate_manager_mock.assert_has_calls(
        [
            call(
                uuid=test_data[0].objects[0].uuid,
                terminate_from=None,
                terminate_to=datetime.date(2023, 1, 1),
            ),
        ]
    )


# OLD tests belows


@pytest.mark.asyncio
@respx.mock
async def test_post_to_listener():
    async with httpx.AsyncClient() as client:
        route = respx.post("https://fakeapi/initiate/terminator/").mock(
            return_value=Response(200)
        )
        response = await client.post("https://fakeapi/initiate/terminator/")
        assert route.called
        assert response.status_code == 200


@pytest.mark.asyncio
@patch(
    "manager_terminator.terminate_managers_init.init_manager_terminator.extract_managers_with_no_persons_or_engagements"
)
@patch("manager_terminator.terminate_managers_init.init_manager_terminator.logger")
async def test_init_when_no_managers_found(
    mock_events_logger, mock_extract_managers_with_no_persons_or_engagements: MagicMock
):
    """
    Tests if function exits correctly, when no manager uuids are found.

    Tests for correct log message and log level.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    mocked_mo_client.get_managers.return_value = (
        MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS
    )
    mock_extract_managers_with_no_persons_or_engagements.return_value = None

    # ACT
    await terminator_initialiser(mocked_mo_client)

    # ASSERT
    mocked_mo_client.terminate_manager.assert_not_awaited()

    mock_events_logger.info.assert_any_call(
        "No manager roles without a person or engagements associated found."
    )


@pytest.mark.asyncio
@patch(
    "manager_terminator.terminate_managers_init.init_manager_terminator.extract_managers_with_no_persons_or_engagements"
)
@patch("manager_terminator.terminate_managers_init.init_manager_terminator.logger")
async def test_terminator_initialiser(
    mock_events_logger,
    mock_extract_managers_uuid_and_end_date: MagicMock,
):
    """
    Tests if the terminate function is awaited.

    Tests for correct log message and log level.
    """
    # ARRANGE
    mocked_mo_client = AsyncMock()
    manager_uuid = UUID("0b51953c-537b-4bf9-a872-2710b0ddd9e3")
    list_of_terminations = [
        {
            "uuid": manager_uuid,
            "termination_date": "2023-09-19",
        }
    ]
    mock_extract_managers_uuid_and_end_date.return_value = list_of_terminations

    # ACT
    await terminator_initialiser(mocked_mo_client)
    for termination_data in list_of_terminations:
        manager_uuid = termination_data.get("uuid")  # type: ignore
        termination_date = termination_data.get("termination_date")
        await mocked_mo_client.terminate_manager(termination_date, manager_uuid)

        # ASSERT
        mocked_mo_client.terminate_manager.assert_awaited_with(
            termination_date, manager_uuid
        )

    # ASSERT
    mock_events_logger.info.assert_any_call(
        "Terminated empty manager(s) with uuid(s):",
        manager_uuids=list_of_terminations,
    )


# Helpers


def _create_test_data_manager_with_employee_engagements(
    manager_validity: GetManagersManagersObjectsObjectsValidity,
    engagement_validities: list[
        GetManagersManagersObjectsObjectsEmployeeEngagementsValidity
    ],
) -> GetManagersManagersObjects:
    org_units = [
        GetManagersManagersObjectsObjectsOrgUnit(
            uuid=uuid4(),
        )
    ]

    return GetManagersManagersObjects(
        objects=[
            GetManagersManagersObjectsObjects(
                uuid=uuid4(),
                employee=[
                    GetManagersManagersObjectsObjectsEmployee(
                        uuid=uuid4(),
                        engagements=[
                            GetManagersManagersObjectsObjectsEmployeeEngagements(
                                uuid=uuid4(),
                                org_unit=org_units,
                                validity=validity_timezone_aware(eng_validity),
                            )
                            for eng_validity in engagement_validities
                        ],
                    ),
                ],
                org_unit=org_units,
                validity=validity_timezone_aware(manager_validity),
            ),
        ]
    )


TEST_DATA_MANAGERS = [
    _create_test_data_manager_with_employee_engagements(
        manager_validity=GetManagersManagersObjectsObjectsValidity(
            from_=datetime.datetime(2023, 1, 1, 0, 0),
            to=datetime.datetime(2023, 12, 31, 0, 0),
        ),
        engagement_validities=[
            # outside/BEFORE manager validity
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2022, 1, 1, 0, 0),
                to=datetime.datetime(2022, 9, 29, 0, 0),
            ),
            # starts outside manager validity, but ends inside
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2022, 12, 1, 0, 0),
                to=datetime.datetime(2023, 3, 1, 0, 0),
            ),
            # completly inside manager validity
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2023, 5, 1, 0, 0),
                to=datetime.datetime(2023, 6, 1, 0, 0),
            ),
            # starts inside manager validity, but ends outside
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2023, 10, 1, 0, 0),
                to=datetime.datetime(2024, 3, 1, 0, 0),
            ),
            # outside/AFTER manager validity
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2024, 6, 1, 0, 0), to=None
            ),
        ],
    ),
    # Test cut of manager validity, if manager validity-from is before engagement validity-from
    # same goes for manager validity-to and engagement validity-to
    _create_test_data_manager_with_employee_engagements(
        manager_validity=GetManagersManagersObjectsObjectsValidity(
            from_=datetime.datetime(2023, 1, 1, 0, 0),
            to=datetime.datetime(2023, 12, 31, 0, 0),
        ),
        engagement_validities=[
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2023, 2, 1, 0, 0),
                to=datetime.datetime(2023, 4, 30, 0, 0),
            ),
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2023, 6, 1, 0, 0),
                to=datetime.datetime(2023, 8, 31, 0, 0),
            ),
            GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(
                from_=datetime.datetime(2023, 10, 1, 0, 0),
                to=datetime.datetime(2023, 11, 30, 0, 0),
            ),
        ],
    ),
]
