from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.project import router as project_router

app = FastAPI()


app.include_router(user_router, tags=['users'])
app.include_router(project_router, tags=['projects'])