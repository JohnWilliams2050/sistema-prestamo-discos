from pydantic import BaseModel
from datetime import date
from typing import Literal, Optional

class RentaCreate(BaseModel):
    cliente_id: str
    disco_id: str

class RentaResponse(BaseModel):
    id: str
    cliente_id: str
    disco_id: str
    fecha_renta: date
    fecha_limite_devolucion: date
    fecha_devolucion_real: Optional[date] = None
    estado: Literal["activa", "devuelta"]