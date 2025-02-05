# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import datetime
from uuid import UUID

import pytest

from manager_terminator.helper_functions import check_for_end_date
from manager_terminator.helper_functions import (
    get_latest_end_date_from_engagement_objects,
)
from manager_terminator.helper_functions import (
    get_manager_uuid_and_manager_end_date_if_in_same_org_unit,
)


@pytest.mark.parametrize(
    "org_unit_test_data, person_object_test_data, expected_result",
    [
        (  # Engagement and manager role not in same org unit and not end date for engagement.
            [{"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}],
            [
                {
                    "uuid": UUID("f5a83fe2-f580-4d3c-90cb-71eb9bf15f7a"),
                    "engagements": [
                        {
                            "uuid": UUID("ffa98442-c6a2-4c03-bbc9-9af95e52528b"),
                            "org_unit": [
                                {"uuid": UUID("ddf55dab-10c4-58eb-ac0f-bef4d980acb0")}
                            ],
                            "validity": {
                                "from_": "2000-03-31T00:00:00+02:00",
                                "to": None,
                            },
                        }
                    ],
                    "manager_roles": [],
                }
            ],
            False,
        ),
        (  # Engagement and manager role in same org unit and there is an end date for engagement.
            [{"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}],
            [
                {
                    "uuid": UUID("f5a83fe2-f580-4d3c-90cb-71eb9bf15f7a"),
                    "engagements": [
                        {
                            "uuid": UUID("ffa98442-c6a2-4c03-bbc9-9af95e52528b"),
                            "org_unit": [
                                {"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}
                            ],
                            "validity": {
                                "from_": "2000-03-31T00:00:00+02:00",
                                "to": "2134-03-31T00:00:00+02:00",
                            },
                        }
                    ],
                    "manager_roles": [],
                }
            ],
            True,
        ),
        (  # Engagement and manager role not in same org unit and end date for engagement.
            [{"uuid": UUID("ddf55dab-10c4-58eb-ac0f-bef4d980acb0")}],
            [
                {
                    "uuid": UUID("f5a83fe2-f580-4d3c-90cb-71eb9bf15f7a"),
                    "engagements": [
                        {
                            "uuid": UUID("ffa98442-c6a2-4c03-bbc9-9af95e52528b"),
                            "org_unit": [
                                {"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}
                            ],
                            "validity": {
                                "from_": "2000-03-31T00:00:00+02:00",
                                "to": "2134-03-31T00:00:00+02:00",
                            },
                        }
                    ],
                    "manager_roles": [],
                }
            ],
            False,
        ),
    ],
)
def test_check_for_end_date(
    org_unit_test_data, person_object_test_data, expected_result
):
    """
    Tests if the check for engagement end date returns the correct boolean.
    True if the engagement has an end.
    False if the engagement has no end date.
    """
    result = check_for_end_date(org_unit_test_data, person_object_test_data)
    assert result == expected_result


@pytest.mark.parametrize(
    "org_unit_uuid_from_person_objects, manager_org_unit_uuid_from_engagement, expected_result",
    [
        (  # ORG UNIT UUID FROM ENGAGEMENTS EMPLOYEE OBJECT.
            [{"uuid": UUID("ddf55dab-10c4-58eb-ac0f-bef4d980acb0")}],
            # ORG UNIT UUID FROM THE ENGAGEMENT OBJECT.
            [{"uuid": UUID("ddf55dab-10c4-58eb-ac0f-bef4d980acb0")}],
            (  # EXPECTED RESULT.
                UUID("cd100ba6-7ccf-4e32-a656-16ae5d6d0cc9"),
                datetime.datetime(
                    2047,
                    4,
                    25,
                    0,
                    0,
                    tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                ),
            ),
        ),
        (  # ORG UNIT UUID FROM ENGAGEMENTS EMPLOYEE OBJECT.
            [{"uuid": UUID("f5a83fe2-f580-4d3c-90cb-71eb9bf15f7a")}],
            # ORG UNIT UUID FROM THE ENGAGEMENT OBJECT.
            [{"uuid": UUID("ddf55dab-10c4-58eb-ac0f-bef4d980acb0")}],
            None,
        ),
        (  # ORG UNIT UUID FROM ENGAGEMENTS EMPLOYEE OBJECT.
            [{"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}],
            # ORG UNIT UUID FROM THE ENGAGEMENT OBJECT.
            [{"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}],
            (  # EXPECTED RESULT.
                UUID("cd100ba6-7ccf-4e32-a656-16ae5d6d0cc9"),
                datetime.datetime(
                    2047,
                    4,
                    25,
                    0,
                    0,
                    tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                ),
            ),
        ),
    ],
)
def test_end_date_in_manager_object(
    org_unit_uuid_from_person_objects,
    manager_org_unit_uuid_from_engagement,
    expected_result,
):
    """
    Tests to retrieve the managers uuid, if the manager role exists in
    the same org unit as the engagement being created/updated/terminated.
    Returns the managers uuid, if it exists in the same org unit.
    """
    test_org_unit_from_person_objects_data = [
        {
            "uuid": UUID("a18c550b-c4ca-4e29-9d56-ad7fb30a8819"),
            "engagements": [
                {
                    "uuid": UUID("0bf38999-c15a-4295-ad9b-ffa4d5087fd9"),
                    "org_unit": [{"uuid": org_unit_uuid_from_person_objects}],
                    "validity": {
                        "from_": datetime.datetime(
                            2017,
                            10,
                            28,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                        "to": datetime.datetime(
                            2047,
                            4,
                            25,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": UUID("cd100ba6-7ccf-4e32-a656-16ae5d6d0cc9"),
                    "org_unit": [{"uuid": org_unit_uuid_from_person_objects}],
                    "validity": {
                        "from_": datetime.datetime(
                            2017,
                            10,
                            28,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                        "to": datetime.datetime(
                            2047,
                            4,
                            25,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                    },
                },
                {
                    "uuid": UUID("ec68a9ee-18e6-409e-891c-83efd5f638b7"),
                    "org_unit": [
                        {"uuid": UUID("fb2d158f-114e-5f67-8365-2c520cf10b58")}
                    ],
                    "validity": {
                        "from_": datetime.datetime(
                            2023,
                            9,
                            19,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                        "to": datetime.datetime(
                            2023,
                            9,
                            19,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
                        ),
                    },
                },
            ],
        }
    ]

    test_org_unit_from_engagement_data = [
        {"uuid": manager_org_unit_uuid_from_engagement, "name": "Renovation"}
    ]

    result = get_manager_uuid_and_manager_end_date_if_in_same_org_unit(
        test_org_unit_from_person_objects_data, test_org_unit_from_engagement_data
    )
    assert result == expected_result


@pytest.mark.parametrize(
    "engagement_end_date_data, manager_end_date_data, expected_result",
    [
        (
            datetime.datetime(
                2043,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),  # ENGAGEMENT END DATE.
            None,  # MANAGER END DATE.
            datetime.datetime(
                2043,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),  # EXPECTED END DATE.
        ),
        (
            datetime.datetime(
                2017,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),  # ENGAGEMENT END DATE.
            datetime.datetime(
                2047,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),  # MANAGER END DATE.
            datetime.datetime(
                2017,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)),
            ),  # EXPECTED END DATE.
        ),
    ],
)
def test_set_latest_end_date_and_ensure_same_org_unit(
    engagement_end_date_data, manager_end_date_data, expected_result
):
    """
    Tests whether the manager roles end date arrives before the engagements end date.
    Will return a datetime string, if the engagement has an earlier end date.
    Will return None, if the manager roles end date arrives before the engagements.
    """
    test_engagement_objects = [
        {
            "uuid": UUID("64c85f9f-ba89-407f-bbb2-7f524ce6a66e"),
            "engagements": [
                {
                    "uuid": UUID("16259667-78ec-4dcf-91bf-84cc1c87243b"),
                    "org_unit": [
                        {"uuid": UUID("5cb38a3c-cacd-5d54-9eb3-88eae2baba1b")}
                    ],
                    "validity": {
                        "from_": datetime.datetime(
                            1978,
                            10,
                            23,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
                        ),
                        "to": engagement_end_date_data,  # From test parameter.
                    },
                }
            ],
            "manager_roles": [
                {
                    "uuid": UUID("73fac2b5-f4c0-4b6a-88bf-8f6f89fe3f42"),
                    "org_unit": [
                        {"uuid": UUID("5cb38a3c-cacd-5d54-9eb3-88eae2baba1b")}
                    ],
                    "validity": {
                        "from_": datetime.datetime(
                            1978,
                            10,
                            23,
                            0,
                            0,
                            tzinfo=datetime.timezone(datetime.timedelta(seconds=3600)),
                        ),
                        "to": manager_end_date_data,
                    },
                }
            ],
        }
    ]
    result = get_latest_end_date_from_engagement_objects(
        test_engagement_objects, manager_end_date_data
    )
    assert result == expected_result
