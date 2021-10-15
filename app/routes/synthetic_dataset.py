from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile
from app.models.datasets import UpdateDataset
from app.services.project import get_project_service
from app.services.model import get_model_service
from app.services.synthetic_dataset import *

from app.utils import get_db

router = APIRouter()

@router.get("/projects/{project_id}/models/{model_id}/synthetic_datasets/{synthetic_dataset_id}", status_code=status.HTTP_200_OK)
async def get_model(project_id: str, model_id: str, synthetic_dataset_id: str, db = Depends(get_db)):
    project = get_project_service(db, project_id)

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    

    model = get_model_service(db, project_id, model_id)
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    synthetic_dataset = get_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id)

    if not synthetic_dataset:
        raise HTTPException(status_code=404, detail="Synthetic Dataset not found")
    return synthetic_dataset

@router.post('/projects/{project_id}/models/{model_id}/synthetic_datasets', status_code=status.HTTP_201_CREATED)
async def create_model(project_id: str, model_id: str, db = Depends(get_db)):

    if not get_project_service(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
      
    if not get_model_service(db, project_id, model_id):
        raise HTTPException(status_code=404, detail="Model not found")

    synthetic_dataset = create_synthetic_dataset_service(db, project_id, model_id)
    if not synthetic_dataset:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return synthetic_dataset

@router.put("/projects/{project_id}/models/{model_id}/synthetic_datasets/{synthetic_dataset_id}", status_code=status.HTTP_200_OK)
async def update_model(project_id: str, model_id: str, synthetic_dataset_id: str, req: UpdateDataset, db = Depends(get_db)):
    if not get_project_service(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not get_model_service(db, project_id, model_id):
        raise HTTPException(status_code=404, detail="Model not found")

    if not check_synthetic_dataset_name_service(db, project_id, model_id, req.name):
        raise HTTPException(status_code=409, detail="Synthetic Dataset with that name in model already exists")

    return update_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id, req)

@router.delete("/projects/{project_id}/models/{model_id}/synthetic_datasets/{synthetic_dataset_id}", status_code=status.HTTP_200_OK)
async def delete_real_dataset(project_id: str, model_id: str, synthetic_dataset_id: str, db = Depends(get_db)):
    if not get_project_service(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not get_model_service(db, project_id, model_id):
        raise HTTPException(status_code=404, detail="Model not found")
    
    if not delete_synthetic_dataset_service(db, project_id, model_id, synthetic_dataset_id):
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return status.HTTP_200_OK

    