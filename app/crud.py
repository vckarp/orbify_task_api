import uuid
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import (Project, ProjectCreate, ProjectPublic, ProjectsPublic,
                     ProjectUpdate)


async def create_project(*, session: AsyncSession, project_create: ProjectCreate) -> Project:
    db_obj = Project.model_validate(project_create)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def update_project(*, session: AsyncSession, db_project: Project, project_update: ProjectUpdate) -> Any:
    project_data = project_update.model_dump(exclude_unset=True)
    if not project_data:
        return None
    db_project.sqlmodel_update(project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_by_id(*, session: AsyncSession, project_id: uuid.UUID) -> ProjectPublic | None:
    statement = select(Project).where(Project.project_id == project_id)
    session_project = await session.exec(statement)
    session_project = session_project.first()
    return session_project


async def get_projects_all(*, session: AsyncSession) -> ProjectsPublic:
    statement = select(Project)
    session_projects = await session.exec(statement)
    session_projects = session_projects.all()
    return ProjectsPublic(data=session_projects)


async def get_projects_by_name(*, session: AsyncSession, name: str) -> ProjectsPublic:
    statement = select(Project).where(Project.name == name)
    session_projects = await session.exec(statement)
    session_projects = session_projects.all()
    return ProjectsPublic(data=session_projects)


async def delete_project(*, session: AsyncSession, db_project: ProjectPublic) -> Project:
    await session.delete(db_project)
    await session.commit()
    return True
