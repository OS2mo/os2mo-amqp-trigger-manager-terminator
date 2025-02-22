# Generated by ariadne-codegen on 2025-02-11 14:25
# Source: queries.graphql

from uuid import UUID

from .base_model import BaseModel


class UpdateManager(BaseModel):
    manager_update: "UpdateManagerManagerUpdate"


class UpdateManagerManagerUpdate(BaseModel):
    uuid: UUID


UpdateManager.update_forward_refs()
UpdateManagerManagerUpdate.update_forward_refs()
