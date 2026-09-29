from pydantic import BaseModel, Field
from typing import Optional

class DiscoBase(BaseModel):
    titulo: str
    artista: str
    genero: str
    anio_lanzamiento: Optional[int] = None

class DiscoCreate(DiscoBase):
    stock_total: int = Field(gt=0)

class DiscoResponse(DiscoBase):
    id: str
    stock_total: int
    stock_disponible: int