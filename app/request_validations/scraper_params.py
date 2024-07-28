from typing import Optional
from pydantic import BaseModel, Field


class ScraperParams(BaseModel):
    url: str = Field(min_length=1)
    pages: Optional[int] = Field(default=5)
    proxy: Optional[str] = None