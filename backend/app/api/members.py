from fastapi import APIRouter, Depends
from app.schemas.member import MemberCreate, MemberResponse
from app.services.member_service import MemberService
from app.repositories.member_repository import MemberRepository

router = APIRouter(prefix="/members", tags=["members"])

def get_member_service() -> MemberService:
    return MemberService(MemberRepository())

def serialize(doc: dict) -> MemberResponse:
    return MemberResponse(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})

@router.post("/", response_model=MemberResponse, status_code=201)
async def create_member(data: MemberCreate, service: MemberService = Depends(get_member_service)):
    doc = await service.create_member(data)
    return serialize(doc)

@router.get("/", response_model=list[MemberResponse])
async def list_members(service: MemberService = Depends(get_member_service)):
    docs = await service.list_members()
    return [serialize(d) for d in docs]

@router.get("/{member_id}", response_model=MemberResponse)
async def get_member(member_id: str, service: MemberService = Depends(get_member_service)):
    doc = await service.get_member(member_id)
    return serialize(doc)
@router.patch("/{member_id}/deactivate", response_model=MemberResponse)
async def deactivate_member(member_id: str, service: MemberService = Depends(get_member_service)):
    doc = await service.deactivate_member(member_id)
    return serialize(doc)