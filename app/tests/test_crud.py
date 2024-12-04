import asyncio
import uuid

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import (create_project, delete_project, get_project_by_id,
                      get_projects_all, get_projects_by_name, update_project)
from app.models import (Project, ProjectCreate, ProjectPublic, ProjectsPublic,
                        ProjectUpdate)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(name="engine")
async def fixture_engine():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(name="session")
async def fixture_session(engine):
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(name="project_create")
def fixture_project_create():
    return ProjectCreate(
        name="Test Project",
        description="Test Description",
        date_start="2022-01-01T00:00:00",
        date_end="2022-12-31T23:59:59",
        area_of_interest={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]})


@pytest.mark.asyncio
async def test_create_project(session: AsyncSession, project_create: ProjectCreate):
    project = await create_project(session=session, project_create=project_create)
    assert project.name == "Test Project"


@pytest.mark.asyncio
async def test_update_project(session: AsyncSession, project_create: ProjectCreate):
    project = await create_project(session=session, project_create=project_create)
    project_update = ProjectUpdate(name="Updated Project")
    updated_project = await update_project(session=session, db_project=project, project_update=project_update)
    assert updated_project.name == "Updated Project"


@pytest.mark.asyncio
async def test_update_project_with_no_changes(session: AsyncSession, project_create: ProjectCreate):
    project = await create_project(session=session, project_create=project_create)
    project_update = ProjectUpdate()
    updated_project = await update_project(session=session, db_project=project, project_update=project_update)
    assert updated_project is None


@pytest.mark.asyncio
async def test_get_project_by_id(session: AsyncSession, project_create: ProjectCreate):
    project = await create_project(session=session, project_create=project_create)
    fetched_project = await get_project_by_id(session=session, project_id=project.project_id)
    assert fetched_project.name == "Test Project"


@pytest.mark.asyncio
async def test_get_project_by_invalid_id(session: AsyncSession):
    invalid_id = uuid.uuid4()
    fetched_project = await get_project_by_id(session=session, project_id=invalid_id)
    assert fetched_project is None


@pytest.mark.asyncio
async def test_get_projects_all(session: AsyncSession, project_create: ProjectCreate):
    await create_project(session=session, project_create=project_create)
    await create_project(session=session, project_create=project_create)
    projects = await get_projects_all(session=session)
    assert len(projects.data) == 2


@pytest.mark.asyncio
async def test_get_projects_by_name(session: AsyncSession, project_create: ProjectCreate):
    await create_project(session=session, project_create=project_create)
    projects = await get_projects_by_name(session=session, name="Test Project")
    assert len(projects.data) == 1
    assert projects.data[0].name == "Test Project"


@pytest.mark.asyncio
async def test_get_projects_by_nonexistent_name(session: AsyncSession):
    projects = await get_projects_by_name(session=session, name="Nonexistent Project")
    assert len(projects.data) == 0


@pytest.mark.asyncio
async def test_delete_project(session: AsyncSession, project_create: ProjectCreate):
    project = await create_project(session=session, project_create=project_create)
    await delete_project(session=session, db_project=project)
    fetched_project = await get_project_by_id(session=session, project_id=project.project_id)
    assert fetched_project is None
