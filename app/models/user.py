from pydantic import BaseModel
from app.models.project import Project
from typing import List, Optional


class NewUser(BaseModel):
    name: str

class User(BaseModel):
    name: str
    projects: List[Project] = [] 

class UpdateUser(BaseModel):
    name: Optional[str] = None