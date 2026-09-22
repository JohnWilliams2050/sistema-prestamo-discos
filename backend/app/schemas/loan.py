from pydantic import BaseModel
from datetime import date

class LoanCreate(BaseModel):
    disc_id: str
    member_id: str

class LoanResponse(BaseModel):
    id: str
    disc_id: str
    member_id: str
    loan_date: date
    due_date: date
    returned: bool