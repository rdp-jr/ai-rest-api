from bson.objectid import ObjectId
from pydantic import BaseModel
from typing import Optional


class NewProject(BaseModel):
    name: str 

class Project(BaseModel):
    id: str = ObjectId()
    name: str 

class UpdateProject(BaseModel):
    name: Optional[str] = None 