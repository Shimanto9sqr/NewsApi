from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HeadlineCreate(BaseModel):
    title: str
    url: str
    summary: Optional[str] = ""
    source: Optional[str] = ""
    published_at: Optional[datetime] = None

class HeadlineRead(BaseModel):
    id: int
    title: str
    url: str
    summary: Optional[str]
    source: Optional[str]
    published_at: Optional[datetime]
    fetched_at: datetime

    model_config = {"from_attributes": True}

