from pydantic import BaseModel, EmailStr
from typing import Optional

class MemberBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    id: str
    active: bool

class MemberResponse(MemberBase):
    id: str
    active: bool