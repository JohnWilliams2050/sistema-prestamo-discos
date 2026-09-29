from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class ClienteBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: str
    estado: Literal["activo", "inactivo"]