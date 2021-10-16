from fastapi import APIRouter, Depends, status, HTTPException
from app.services.user import *
from app.models.user import *

from app.utils import get_db
from app.config import logged_in_user_id

router = APIRouter()

@router.get("/users")
async def index(db = Depends(get_db)):
    return get_users_service(db)

@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db = Depends(get_db)):
    
    user = get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/dashboard", status_code=status.HTTP_200_OK)
async def dashboard(db = Depends(get_db)):
    user = get_user_service(db, logged_in_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post('/users', status_code=status.HTTP_201_CREATED)
async def create_user(req: NewUser, db = Depends(get_db)):
    result = create_user_service(db, req)
    if not result:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Create user failed")
    return result

@router.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, req: UpdateUser, db = Depends(get_db)):
    return update_user_service(db, user_id, req)

@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str, db = Depends(get_db)):
    user = get_user_service(db, logged_in_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    if not delete_user_service(db, user_id):
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return status.HTTP_200_OK