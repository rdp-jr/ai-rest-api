from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from app.services.project import get_project_service
from app.services.real_dataset import *
from app.models.datasets import *

from app.utils import get_db

router = APIRouter()

@router.get("/projects/{project_id}/real_datasets/{real_dataset_id}", status_code=status.HTTP_200_OK)
async def get_real_dataset(project_id: str, real_dataset_id: str, db = Depends(get_db)):
    real_dataset = get_real_dataset_service(db, project_id, real_dataset_id)

    if not real_dataset:
        raise HTTPException(status_code=404, detail="real_dataset not found")
    return real_dataset

@router.post('/projects/{project_id}/real_datasets', status_code=status.HTTP_201_CREATED)
async def create_real_dataset(project_id: str, file: UploadFile = File(...), db = Depends(get_db)):
    project = get_project_service(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return create_real_dataset_service(db, project_id, file)

@router.put("/projects/{project_id}/real_datasets/{real_dataset_id}", status_code=status.HTTP_200_OK)
async def update_real_dataset(project_id: str, real_dataset_id: str, req: UpdateDataset, db = Depends(get_db)):
    if not get_real_dataset_service(db, project_id, real_dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if not check_real_dataset_name_service(db, project_id, req.name):
        raise HTTPException(status_code=409, detail="Dataset with that name in project already exists")

    return update_real_dataset_service(db, project_id, real_dataset_id, req)

@router.delete("/projects/{project_id}/real_datasets/{real_dataset_id}", status_code=status.HTTP_200_OK)
async def delete_real_dataset(project_id: str, real_dataset_id: str, db = Depends(get_db)):
    if not get_real_dataset_service(db, project_id, real_dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    if not delete_real_dataset_service(db, project_id, real_dataset_id):
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return status.HTTP_200_OK

    