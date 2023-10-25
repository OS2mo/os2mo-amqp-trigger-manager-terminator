# Generated by ariadne-codegen on 2023-10-25 16:12
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetManagers(BaseModel):
    managers: "GetManagersManagers"


class GetManagersManagers(BaseModel):
    objects: List["GetManagersManagersObjects"]


class GetManagersManagersObjects(BaseModel):
    objects: List["GetManagersManagersObjectsObjects"]


class GetManagersManagersObjectsObjects(BaseModel):
    uuid: UUID
    org_unit: List["GetManagersManagersObjectsObjectsOrgUnit"]
    employee: Optional[List["GetManagersManagersObjectsObjectsEmployee"]]
    validity: "GetManagersManagersObjectsObjectsValidity"


class GetManagersManagersObjectsObjectsOrgUnit(BaseModel):
    uuid: UUID


class GetManagersManagersObjectsObjectsEmployee(BaseModel):
    engagements: List["GetManagersManagersObjectsObjectsEmployeeEngagements"]


class GetManagersManagersObjectsObjectsEmployeeEngagements(BaseModel):
    uuid: UUID
    org_unit: List["GetManagersManagersObjectsObjectsEmployeeEngagementsOrgUnit"]
    validity: "GetManagersManagersObjectsObjectsEmployeeEngagementsValidity"


class GetManagersManagersObjectsObjectsEmployeeEngagementsOrgUnit(BaseModel):
    uuid: UUID


class GetManagersManagersObjectsObjectsEmployeeEngagementsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetManagersManagersObjectsObjectsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetManagers.update_forward_refs()
GetManagersManagers.update_forward_refs()
GetManagersManagersObjects.update_forward_refs()
GetManagersManagersObjectsObjects.update_forward_refs()
GetManagersManagersObjectsObjectsOrgUnit.update_forward_refs()
GetManagersManagersObjectsObjectsEmployee.update_forward_refs()
GetManagersManagersObjectsObjectsEmployeeEngagements.update_forward_refs()
GetManagersManagersObjectsObjectsEmployeeEngagementsOrgUnit.update_forward_refs()
GetManagersManagersObjectsObjectsEmployeeEngagementsValidity.update_forward_refs()
GetManagersManagersObjectsObjectsValidity.update_forward_refs()
