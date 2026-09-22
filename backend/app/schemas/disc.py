from pydantic import BaseModel, Field
from typing import Optional

class DiscBase(BaseModel):
    title: str
    artist: str
    genre: str
    format: str  # "CD", "Vinyl", "Cassette"

class DiscCreate(DiscBase):
    total_copies: int = Field(gt=0)

class DiscResponse(DiscBase):
    id: str
    total_copies: int
    available_copies: int