# Generated by ariadne-codegen on 2025-02-05 10:52
# Source: queries.graphql

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEngagementObjectsByUuids(BaseModel):
    engagements: "GetEngagementObjectsByUuidsEngagements"


class GetEngagementObjectsByUuidsEngagements(BaseModel):
    objects: List["GetEngagementObjectsByUuidsEngagementsObjects"]


class GetEngagementObjectsByUuidsEngagementsObjects(BaseModel):
    validities: List["GetEngagementObjectsByUuidsEngagementsObjectsValidities"]


class GetEngagementObjectsByUuidsEngagementsObjectsValidities(BaseModel):
    uuid: UUID
    org_unit: List["GetEngagementObjectsByUuidsEngagementsObjectsValiditiesOrgUnit"]
    person: List["GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPerson"]
    validity: "GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity"


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesOrgUnit(BaseModel):
    uuid: UUID


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPerson(BaseModel):
    uuid: UUID


class GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEngagementObjectsByUuids.update_forward_refs()
GetEngagementObjectsByUuidsEngagements.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjects.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValidities.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesOrgUnit.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesPerson.update_forward_refs()
GetEngagementObjectsByUuidsEngagementsObjectsValiditiesValidity.update_forward_refs()
