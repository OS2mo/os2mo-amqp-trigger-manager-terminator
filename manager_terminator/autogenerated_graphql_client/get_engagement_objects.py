# Generated by ariadne-codegen on 2023-10-25 16:12
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEngagementObjects(BaseModel):
    engagements: "GetEngagementObjectsEngagements"


class GetEngagementObjectsEngagements(BaseModel):
    objects: List["GetEngagementObjectsEngagementsObjects"]


class GetEngagementObjectsEngagementsObjects(BaseModel):
    objects: List["GetEngagementObjectsEngagementsObjectsObjects"]


class GetEngagementObjectsEngagementsObjectsObjects(BaseModel):
    org_unit: List["GetEngagementObjectsEngagementsObjectsObjectsOrgUnit"]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsValidity"
    employee: List["GetEngagementObjectsEngagementsObjectsObjectsEmployee"]


class GetEngagementObjectsEngagementsObjectsObjectsOrgUnit(BaseModel):
    uuid: UUID
    name: str


class GetEngagementObjectsEngagementsObjectsObjectsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEngagementObjectsEngagementsObjectsObjectsEmployee(BaseModel):
    uuid: UUID
    engagements: List[
        "GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagements"
    ]
    manager_roles: List[
        "GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRoles"
    ]


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagements(BaseModel):
    uuid: UUID
    org_unit: List[
        "GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsOrgUnit"
    ]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsValidity"


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsOrgUnit(
    BaseModel
):
    uuid: UUID


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsValidity(
    BaseModel
):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRoles(BaseModel):
    uuid: UUID
    org_unit: List[
        "GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesOrgUnit"
    ]
    validity: "GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesValidity"


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesOrgUnit(
    BaseModel
):
    uuid: UUID


class GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesValidity(
    BaseModel
):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEngagementObjects.update_forward_refs()
GetEngagementObjectsEngagements.update_forward_refs()
GetEngagementObjectsEngagementsObjects.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjects.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsValidity.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployee.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagements.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeEngagementsValidity.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRoles.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesOrgUnit.update_forward_refs()
GetEngagementObjectsEngagementsObjectsObjectsEmployeeManagerRolesValidity.update_forward_refs()
