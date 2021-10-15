from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import List, Optional

class NewProject(BaseModel):
    name: str 

class Project(BaseModel):
    id: str = ObjectId()
    name: str 
    models: List[str] = []
    real_datasets: List[str] = []

class UpdateProject(BaseModel):
    name: Optional[str] = None 