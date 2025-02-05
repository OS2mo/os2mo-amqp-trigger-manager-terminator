# Generated by ariadne-codegen on 2025-02-05 10:52
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .get_employee_managers import GetEmployeeManagers, GetEmployeeManagersManagers
from .get_engagement_objects import (
    GetEngagementObjects,
    GetEngagementObjectsEngagements,
)
from .get_engagement_objects_by_uuids import (
    GetEngagementObjectsByUuids,
    GetEngagementObjectsByUuidsEngagements,
)
from .get_managers import GetManagers, GetManagersManagers
from .terminate_manager import TerminateManager, TerminateManagerManagerTerminate
from .update_manager import UpdateManager, UpdateManagerManagerUpdate


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):

    async def get_managers(self) -> GetManagersManagers:
        query = gql(
            """
            query GetManagers {
              managers(filter: {from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                    org_unit {
                      uuid
                    }
                    person {
                      engagements {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetManagers.parse_obj(data).managers

    async def terminate_manager(
        self,
        uuid: UUID,
        terminate_to: datetime,
        terminate_from: Union[Optional[datetime], UnsetType] = UNSET,
    ) -> TerminateManagerManagerTerminate:
        query = gql(
            """
            mutation TerminateManager($uuid: UUID!, $terminate_from: DateTime, $terminate_to: DateTime!) {
              manager_terminate(
                input: {uuid: $uuid, from: $terminate_from, to: $terminate_to}
              ) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {
            "uuid": uuid,
            "terminate_from": terminate_from,
            "terminate_to": terminate_to,
        }
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TerminateManager.parse_obj(data).manager_terminate

    async def update_manager(
        self, uuid: UUID, vacant_from: datetime
    ) -> UpdateManagerManagerUpdate:
        query = gql(
            """
            mutation UpdateManager($uuid: UUID!, $vacant_from: DateTime!) {
              manager_update(input: {uuid: $uuid, from: $vacant_from, person: null}) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid, "vacant_from": vacant_from}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UpdateManager.parse_obj(data).manager_update

    async def get_engagement_objects(
        self, engagement_uuid: UUID
    ) -> GetEngagementObjectsEngagements:
        query = gql(
            """
            query GetEngagementObjects($engagement_uuid: UUID!) {
              engagements(filter: {uuids: [$engagement_uuid]}) {
                objects {
                  validities {
                    org_unit {
                      uuid
                      name
                    }
                    validity {
                      from
                      to
                    }
                    person {
                      uuid
                      engagements {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                      manager_roles {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"engagement_uuid": engagement_uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEngagementObjects.parse_obj(data).engagements

    async def get_engagement_objects_by_uuids(
        self, engagement_uuids: List[UUID]
    ) -> GetEngagementObjectsByUuidsEngagements:
        query = gql(
            """
            query GetEngagementObjectsByUuids($engagement_uuids: [UUID!]!) {
              engagements(filter: {uuids: $engagement_uuids, from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                    org_unit {
                      uuid
                    }
                    person {
                      uuid
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"engagement_uuids": engagement_uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEngagementObjectsByUuids.parse_obj(data).engagements

    async def get_employee_managers(
        self, employee_uuids: List[UUID]
    ) -> GetEmployeeManagersManagers:
        query = gql(
            """
            query GetEmployeeManagers($employee_uuids: [UUID!]!) {
              managers(filter: {employees: $employee_uuids, from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                    org_unit {
                      uuid
                    }
                    person {
                      engagements {
                        uuid
                        org_unit {
                          uuid
                        }
                        validity {
                          from
                          to
                        }
                      }
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"employee_uuids": employee_uuids}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeManagers.parse_obj(data).managers
