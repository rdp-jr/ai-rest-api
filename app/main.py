from fastapi import FastAPI
from app.routes.user import router as user_router
from app.routes.project import router as project_router
from app.routes.real_dataset import router as real_dataset_router
from app.routes.model import router as model_router
from app.routes.synthetic_dataset import router as synthetic_dataset_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, tags=['users'])
app.include_router(project_router, tags=['projects'])
app.include_router(real_dataset_router, tags=['real_datasets'])
app.include_router(model_router, tags=['models'])
app.include_router(synthetic_dataset_router, tags=['synthetic_datasets'])