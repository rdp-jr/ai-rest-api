from fastapi import APIRouter, Depends, status, HTTPException
from app.services.user import *
from app.models.user import User

from app.config import db as conn

def get_db():
    yield conn

router = APIRouter()

@router.get("/")
async def index(db = Depends(get_db)):
    return get_users(db)

@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(req: User, db = Depends(get_db)):
    if not insert_user(db, req):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Create user failed")
    return status.HTTP_201_CREATED