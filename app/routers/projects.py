import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from ..crud import (create_project, delete_project, get_project_by_id,
                    get_projects_all, get_projects_by_name, update_project)
from ..deps import SessionDep
from ..models import (Message, ProjectCreate, ProjectPublic, ProjectsPublic,
                      ProjectUpdate)

router = APIRouter(tags=["projects"])


@router.get("/list/all", response_model=ProjectsPublic)
async def read_projects_all(session: SessionDep = SessionDep) -> Any:
    projects_list = await get_projects_all(session=session)
    if not projects_list:
        raise HTTPException(status_code=404, detail="No projects found")
    return projects_list


@router.get("/list/{name}", response_model=ProjectsPublic)
async def read_projects_by_name(name: str, session: SessionDep = SessionDep) -> Any:
    projects_list = await get_projects_by_name(session=session, name=name)
    if not projects_list:
        raise HTTPException(status_code=404, detail=f"Projects with name '{name}' not found")
    return projects_list


@router.get("/read/{project_id}", response_model=ProjectPublic)
async def read_project_by_id(project_id: uuid.UUID, session: SessionDep = SessionDep) -> Any:
    project = await get_project_by_id(session=session, project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project of id '{project_id}' not found")
    return project


@router.post("/create", response_model=ProjectPublic)
async def create_new_project(project_create: ProjectCreate, session: SessionDep = SessionDep) -> Any:
    new_project = await create_project(session=session, project_create=project_create)
    return new_project


@router.patch("/update/{project_id}", response_model=ProjectPublic)
async def update_existing_project(
    project_id: uuid.UUID, project_update: ProjectUpdate, session: SessionDep = SessionDep
) -> Any:
    db_project = await get_project_by_id(session=session, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    response = await update_project(session=session, db_project=db_project, project_update=project_update)
    if not response:
        raise HTTPException(status_code=400, detail="No data to update")
    return response


@router.delete("/delete/{project_id}")
async def delete_existing_project(project_id: uuid.UUID, session: SessionDep = SessionDep) -> Any:
    db_project = await get_project_by_id(session=session, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    await delete_project(session=session, db_project=db_project)
    return Message(message="Project deleted")
