from shortuuid import ShortUUID
from pydantic import BaseModel
from typing import List, Optional
from app.models.datasets import Dataset

class ModelParameter(BaseModel):
    batch_size: int
    training_cycles: int

class NewModel(BaseModel):
    name: str 
    parameters: ModelParameter

class UpdateModel(BaseModel):
    name: Optional[str] = None 

class Model(BaseModel):
    id: str = ShortUUID().random(length=5)
    name: str 
    parameters: ModelParameter
    synthetic_datasets: Optional[List[Dataset]] = []

