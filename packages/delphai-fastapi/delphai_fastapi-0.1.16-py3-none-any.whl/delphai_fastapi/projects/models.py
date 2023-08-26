from typing import List, Optional

from fastapi_camelcase import CamelModel
from pydantic import Field
from datetime import datetime
from ..types import ObjectId


class Project(CamelModel):
    id: ObjectId = Field(..., description="Internal project ID")
    total: int = Field(
        ..., description="Total number of companies in this project", example=35
    )
    name: str = Field(
        ..., description="Name of the project", example="Healthcare | Startups"
    )
    created: datetime = Field(..., description="When the project was created")
    created_by: str = Field(..., description="ID of the user who created the project")
    client: str = Field(..., description="ID of the client who owns the project")
    last_modified: datetime = Field(
        ..., description="When the project was last edited or updated"
    )
    parent_project: Optional[ObjectId] = Field(
        description="Internal project ID of parent project"
    )


class Projects(CamelModel):
    results: List[Project]
    total: int = Field(..., description="Number of results")
