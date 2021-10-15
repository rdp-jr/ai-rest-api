from pydantic import BaseModel
from typing import Optional
from shortuuid import ShortUUID
# from pydantic.networks import HttpUrl

class Dataset(BaseModel):
    id: str = ShortUUID().random(length=5)
    name: str
    # use HttpUrl type for production
    url: str

class UpdateRealDataset(BaseModel):
    project_id: Optional[str] = None
    dataset_name: Optional[str] = None

class UpdateDataset(BaseModel):
    name: Optional[str] = None