import uuid
from datetime import datetime

from sqlmodel import JSON, TIMESTAMP, Column, Field, SQLModel


class Message(SQLModel):
    message: str


class ProjectBase(SQLModel):
    name: str = Field(max_length=32)
    description: str | None = Field(default=None)
    date_start: datetime = Field(sa_column=Column(TIMESTAMP()))
    date_end: datetime = Field(sa_column=Column(TIMESTAMP()))
    area_of_interest: dict = Field(sa_column=Column(JSON))


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase, table=True):
    project_id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)


class ProjectUpdate(ProjectBase):
    name: str | None = Field(default=None, max_length=32)
    date_start: datetime | None = None
    date_end: datetime | None = None
    area_of_interest: dict | None = None


class ProjectPublic(ProjectBase):
    project_id: uuid.UUID


class ProjectsPublic(SQLModel):
    data: list[ProjectPublic]
