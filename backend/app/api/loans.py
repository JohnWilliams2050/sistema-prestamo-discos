from fastapi import APIRouter, Depends
from app.schemas.loan import LoanCreate, LoanResponse
from app.services.loan_service import LoanService
from app.repositories.loan_repository import LoanRepository
from app.repositories.disc_repository import DiscRepository
from app.repositories.member_repository import MemberRepository

router = APIRouter(prefix="/loans", tags=["loans"])

def get_loan_service() -> LoanService:
    return LoanService(LoanRepository(), DiscRepository(), MemberRepository())

def serialize(doc: dict) -> LoanResponse:
    return LoanResponse(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})

@router.post("/", response_model=LoanResponse, status_code=201)
async def create_loan(data: LoanCreate, service: LoanService = Depends(get_loan_service)):
    doc = await service.create_loan(data)
    return serialize(doc)

@router.get("/", response_model=list[LoanResponse])
async def list_loans(service: LoanService = Depends(get_loan_service)):
    docs = await service.list_loans()
    return [serialize(d) for d in docs]