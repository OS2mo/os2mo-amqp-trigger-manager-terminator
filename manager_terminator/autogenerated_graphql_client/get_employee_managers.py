# Generated by ariadne-codegen on 2023-10-31 13:27
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEmployeeManagers(BaseModel):
    managers: "GetEmployeeManagersManagers"


class GetEmployeeManagersManagers(BaseModel):
    objects: List["GetEmployeeManagersManagersObjects"]


class GetEmployeeManagersManagersObjects(BaseModel):
    objects: List["GetEmployeeManagersManagersObjectsObjects"]


class GetEmployeeManagersManagersObjectsObjects(BaseModel):
    uuid: UUID
    org_unit: List["GetEmployeeManagersManagersObjectsObjectsOrgUnit"]
    person: Optional[List["GetEmployeeManagersManagersObjectsObjectsPerson"]]
    validity: "GetEmployeeManagersManagersObjectsObjectsValidity"


class GetEmployeeManagersManagersObjectsObjectsOrgUnit(BaseModel):
    uuid: UUID


class GetEmployeeManagersManagersObjectsObjectsPerson(BaseModel):
    engagements: List["GetEmployeeManagersManagersObjectsObjectsPersonEngagements"]


class GetEmployeeManagersManagersObjectsObjectsPersonEngagements(BaseModel):
    uuid: UUID
    org_unit: List["GetEmployeeManagersManagersObjectsObjectsPersonEngagementsOrgUnit"]
    validity: "GetEmployeeManagersManagersObjectsObjectsPersonEngagementsValidity"


class GetEmployeeManagersManagersObjectsObjectsPersonEngagementsOrgUnit(BaseModel):
    uuid: UUID


class GetEmployeeManagersManagersObjectsObjectsPersonEngagementsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEmployeeManagersManagersObjectsObjectsValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEmployeeManagers.update_forward_refs()
GetEmployeeManagersManagers.update_forward_refs()
GetEmployeeManagersManagersObjects.update_forward_refs()
GetEmployeeManagersManagersObjectsObjects.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsOrgUnit.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsPerson.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsPersonEngagements.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsPersonEngagementsOrgUnit.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsPersonEngagementsValidity.update_forward_refs()
GetEmployeeManagersManagersObjectsObjectsValidity.update_forward_refs()