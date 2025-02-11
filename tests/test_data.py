# SPDX-FileCopyrightText: 2023 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from uuid import UUID

NO_ENGAGEMENT_OBJECTS_FOUND = {"objects": []}

ENGAGEMENT_OBJECTS = {
    "objects": [
        {
            "validities": [
                {
                    "org_unit": [
                        {
                            "uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9"),
                            "name": "Kolding Kommune",
                        }
                    ],
                    "validity": {
                        "from_": "1972-04-27T00:00:00+01:00",
                        "to": None,
                    },
                    "person": [
                        {
                            "uuid": UUID("9387b721-5a26-4aa3-842d-55e3a1fa2d3e"),
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "f06ee470-9f17-566f-acbe-e938112d46d9"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": "2023-09-20T00:00:00+02:00",
                                    },
                                }
                            ],
                            "manager_roles": [
                                {
                                    "uuid": UUID(
                                        "29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "f06ee470-9f17-566f-acbe-e938112d46d9"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": None,
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    ]
}


ENGAGEMENT_OBJECTS_PERSON_IS_NOT_MANAGER = {
    "objects": [
        {
            "validities": [
                {
                    "org_unit": [
                        {
                            "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                            "name": "Kolding Kommune",
                        }
                    ],
                    "validity": {
                        "from_": "1972-04-27T00:00:00+01:00",
                        "to": None,
                    },
                    "person": [
                        {
                            "uuid": "9387b721-5a26-4aa3-842d-55e3a1fa2d3e",
                            "engagements": [
                                {
                                    "uuid": "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": "2023-09-20T00:00:00+02:00",
                                    },
                                }
                            ],
                            "manager_roles": [],
                        }
                    ],
                }
            ]
        }
    ]
}


ENGAGEMENT_OBJECTS_NO_END_DATE_IN_ENGAGEMENT = {
    "objects": [
        {
            "validities": [
                {
                    "org_unit": [
                        {
                            "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                            "name": "Kolding Kommune",
                        }
                    ],
                    "validity": {
                        "from_": "1972-04-27T00:00:00+01:00",
                        "to": None,
                    },
                    "person": [
                        {
                            "uuid": "9387b721-5a26-4aa3-842d-55e3a1fa2d3e",
                            "engagements": [
                                {
                                    "uuid": "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": None,
                                    },
                                }
                            ],
                            "manager_roles": [
                                {
                                    "uuid": "29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": None,
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    ]
}

ENGAGEMENT_OBJECTS_MANAGER_WITH_EARLIER_END_DATE_THAN_ENGAGEMENT_END_DATE = {
    "objects": [
        {
            "validities": [
                {
                    "org_unit": [
                        {
                            "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                            "name": "Kolding Kommune",
                        }
                    ],
                    "validity": {
                        "from_": "1972-04-27T00:00:00+01:00",
                        "to": None,
                    },
                    "person": [
                        {
                            "uuid": "9387b721-5a26-4aa3-842d-55e3a1fa2d3e",
                            "engagements": [
                                {
                                    "uuid": "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": "2023-09-20T00:00:00+02:00",
                                    },
                                }
                            ],
                            "manager_roles": [
                                {
                                    "uuid": "29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "1972-04-27T00:00:00+01:00",
                                        "to": "2022-09-20T00:00:00+02:00",
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    ]
}


ENGAGEMENT_OBJECTS_MANAGER_AND_ENGAGEMENT_NOT_IN_SAME_ORG_UNIT = {
    "objects": [
        {
            "validities": [
                {
                    "org_unit": [
                        {
                            "uuid": "f06ee470-9f17-566f-acbe-e938112d46d9",
                            "name": "Borgmesterens Afdeling",
                        }
                    ],
                    "validity": {
                        "from_": "2023-09-20T00:00:00+02:00",
                        "to": "2023-09-29T00:00:00+02:00",
                    },
                    "person": [
                        {
                            "uuid": "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54",
                            "engagements": [
                                {
                                    "uuid": "141c39db-7ce0-4332-b4e4-a4d2114b0f51",
                                    "org_unit": [
                                        {"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}
                                    ],
                                    "validity": {
                                        "from_": "2023-09-20T00:00:00+02:00",
                                        "to": "2023-09-29T00:00:00+02:00",
                                    },
                                }
                            ],
                            "manager_roles": [
                                {
                                    "uuid": "7c27c18f-9f5f-43c4-bfe0-b87421db4a59",
                                    "org_unit": [
                                        {"uuid": "b6c11152-0645-4712-a207-ba2c53b391ab"}
                                    ],
                                    "validity": {
                                        "from_": "2006-03-30T00:00:00+02:00",
                                        "to": None,
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    ]
}


EMPLOYEE_OBJECTS = {
    "uuid": "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54",
    "engagements": [
        {
            "uuid": "141c39db-7ce0-4332-b4e4-a4d2114b0f51",
            "org_unit": [{"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}],
            "validity": {
                "from_": "1972-04-27T00:00:00+01:00",
                "to": "2023-09-29T00:00:00+02:00",
            },
        }
    ],
    "manager_roles": [
        {
            "uuid": "7c27c18f-9f5f-43c4-bfe0-b87421db4a59",
            "org_unit": [{"uuid": "f06ee470-9f17-566f-acbe-e938112d46d9"}],
            "validity": {
                "from_": "2006-03-30T00:00:00+02:00",
                "to": None,
            },
        }
    ],
}


ENGAGEMENT_ORG_UNIT_OBJECTS = {
    "uuid": "b6c11152-0645-4712-a207-ba2c53b391ab",
    "name": "Borgmesterens Afdeling",
}


MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL_NO_ENGAGEMENTS = {
    "objects": [
        {
            "validities": [
                {
                    "uuid": "0b51953c-537b-4bf9-a872-2710b0ddd9e3",
                    "org_unit": [{"uuid": "13f3cebf-2625-564a-bcfc-31272eb9bce2"}],
                    "person": [],
                    "validity": {
                        "from": "1975-12-08T00:00:00+01:00",
                        "to": None,
                    },
                }
            ]
        }
    ]
}

ALL_MANAGER_OBJECTS_FROM_GET_MANAGERS_CALL = {
    "objects": [
        {
            "validities": [
                {
                    "uuid": UUID("0b51953c-537b-4bf9-a872-2710b0ddd9e3"),
                    "org_unit": [
                        {"uuid": UUID("13f3cebf-2625-564a-bcfc-31272eb9bce2")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "ef9f76fd-1840-4d94-961a-1140c86efd00"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "13f3cebf-2625-564a-bcfc-31272eb9bce2"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1975,
                                            12,
                                            8,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1975, 12, 8, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("106c048f-cfdc-42b4-a418-d5e40b070451"),
                    "org_unit": [
                        {"uuid": UUID("7764d0c7-e776-5f07-8a9d-5ee6f5b717b0")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "8f1d1aac-285b-4284-ae58-35aaf944b974"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "7764d0c7-e776-5f07-8a9d-5ee6f5b717b0"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1985,
                                            11,
                                            15,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1985, 11, 15, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("220c2015-1da8-4850-9c0e-78ed4947f540"),
                    "org_unit": [
                        {"uuid": UUID("2665d8e0-435b-5bb6-a550-f275692984ef")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "5224902e-eca4-42a8-b379-ca55a7a1fceb"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "2665d8e0-435b-5bb6-a550-f275692984ef"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1986,
                                            1,
                                            14,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1986, 1, 14, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("2725d6c8-b293-486f-8cc4-2e9aa09c1e7f"),
                    "org_unit": [
                        {"uuid": UUID("cf4daae1-4812-41f1-8c47-63a99e26aadf")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "49a41fa8-b85a-4ba2-953d-db0a50590fd7"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "cf4daae1-4812-41f1-8c47-63a99e26aadf"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1965,
                                            1,
                                            4,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1965, 1, 4, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("29aaf8f7-4bc2-4d3d-ba8f-ed9fd457c101"),
                    "org_unit": [
                        {"uuid": UUID("f06ee470-9f17-566f-acbe-e938112d46d9")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "f06ee470-9f17-566f-acbe-e938112d46d9"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1972,
                                            4,
                                            27,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": datetime(
                                            2023,
                                            9,
                                            18,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=7200)),
                                        ),
                                    },
                                },
                                {
                                    "uuid": UUID(
                                        "fa5e2af6-ae28-4b6b-8895-3b7d39f93d54"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "f06ee470-9f17-566f-acbe-e938112d46d9"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            2023,
                                            9,
                                            19,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=7200)),
                                        ),
                                        "to": None,
                                    },
                                },
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1972, 4, 27, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("2e9a7dff-4eed-4060-b746-cbf8e224bfb4"),
                    "org_unit": [
                        {"uuid": UUID("6fc9ba6b-ca5b-5e09-a594-40363c45aae0")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "44bdf5f3-f821-4c7e-ad18-48c653700299"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "6fc9ba6b-ca5b-5e09-a594-40363c45aae0"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1968,
                                            8,
                                            16,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1968, 8, 16, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
        {
            "validities": [
                {
                    "uuid": UUID("305d25f5-badb-4aa9-8d94-73d92c2bed35"),
                    "org_unit": [
                        {"uuid": UUID("327301c2-fdab-5773-9357-d0df0548258e")}
                    ],
                    "person": [
                        {
                            "engagements": [
                                {
                                    "uuid": UUID(
                                        "f9d88742-c46a-4570-9f30-f66713fd4d8a"
                                    ),
                                    "org_unit": [
                                        {
                                            "uuid": UUID(
                                                "327301c2-fdab-5773-9357-d0df0548258e"
                                            )
                                        }
                                    ],
                                    "validity": {
                                        "from": datetime(
                                            1987,
                                            2,
                                            8,
                                            0,
                                            0,
                                            tzinfo=timezone(timedelta(seconds=3600)),
                                        ),
                                        "to": None,
                                    },
                                }
                            ]
                        }
                    ],
                    "validity": {
                        "from": datetime(
                            1987, 2, 8, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
                        ),
                        "to": None,
                    },
                }
            ]
        },
    ]
}
