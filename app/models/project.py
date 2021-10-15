from shortuuid import ShortUUID
from pydantic import BaseModel
from typing import List, Optional
from app.models.datasets import Dataset
from app.models.model import Model

class NewProject(BaseModel):
    name: str 

class Project(BaseModel):
    id: str = ShortUUID().random(length=5)
    name: str 
    models: List[Model] = []
    real_datasets: List[Dataset] = []

class UpdateProject(BaseModel):
    name: Optional[str] = None 