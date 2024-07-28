from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimeStamps(BaseModel):
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)