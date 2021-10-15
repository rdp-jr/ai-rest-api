from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from app.services.project import get_project_service
from app.services.model import *
from app.models.model import *

from app.utils import get_db

router = APIRouter()

@router.get("/projects/{project_id}/models/{model_id}", status_code=status.HTTP_200_OK)
async def get_model(project_id: str, model_id: str, db = Depends(get_db)):
    model = get_model_service(db, project_id, model_id)

    if not model:
        raise HTTPException(status_code=404, detail="model not found")
    return model

@router.post('/projects/{project_id}/models', status_code=status.HTTP_201_CREATED)
async def create_model(project_id: str, req: NewModel, db = Depends(get_db)):

    if not check_model_name_service(db, project_id, req.name):
        raise HTTPException(status_code=409, detail="Model with that name in project already exists")
        
    project = get_project_service(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    

    model = create_model_service(db, project_id, req)
    if not model:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return model

@router.put("/projects/{project_id}/models/{model_id}", status_code=status.HTTP_200_OK)
async def update_model(project_id: str, model_id: str, req: UpdateModel, db = Depends(get_db)):
    if not get_model_service(db, project_id, model_id):
        raise HTTPException(status_code=404, detail="Model not found")

    if not check_model_name_service(db, project_id, req.name):
        raise HTTPException(status_code=409, detail="Model with that name in project already exists")

    return update_model_service(db, project_id, model_id, req)

@router.delete("/projects/{project_id}/models/{model_id}", status_code=status.HTTP_200_OK)
async def delete_model(project_id: str, model_id: str, db = Depends(get_db)):
    if not get_model_service(db, project_id, model_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if not delete_model_service(db, project_id, model_id):
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return status.HTTP_200_OK

    