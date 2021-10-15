from fastapi import APIRouter, Depends, status, HTTPException
from app.services.project import *
from app.models.project import *

from app.utils import get_db

router = APIRouter()

@router.get("/projects")
async def index(db = Depends(get_db)):
    projects = get_projects_service(db)

    if not projects:
        raise HTTPException(status_code=404, detail="User not found")
    return projects

@router.get("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def get_project(project_id: str, db = Depends(get_db)):
    project = get_project_service(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post('/projects', status_code=status.HTTP_201_CREATED)
async def create_project(req: NewProject, db = Depends(get_db)):
    if not check_project_name_service(db, req.name):
        raise HTTPException(status_code=409, detail="Project with that name already exists")

    return create_project_service(db, req)

@router.put("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def update_project(project_id: str, req: UpdateProject, db = Depends(get_db)):
    if not get_project_service(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not check_project_name_service(db, req.name):
        raise HTTPException(status_code=409, detail="Project with that name already exists")
    update_project_service(db, project_id, req)
    