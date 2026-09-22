from fastapi import APIRouter, Depends
from app.schemas.disc import DiscCreate, DiscResponse
from app.services.disc_service import DiscService, DiscNotFoundError
from app.repositories.disc_repository import DiscRepository

router = APIRouter(prefix="/discs", tags=["discs"])

def get_disc_service() -> DiscService:
    return DiscService(DiscRepository())

def serialize(doc: dict) -> DiscResponse:
    return DiscResponse(id=str(doc["_id"]), **{k: v for k, v in doc.items() if k != "_id"})

@router.post("/", response_model=DiscResponse, status_code=201)
async def create_disc(data: DiscCreate, service: DiscService = Depends(get_disc_service)):
    doc = await service.create_disc(data)
    return serialize(doc)

@router.get("/", response_model=list[DiscResponse])
async def list_discs(service: DiscService = Depends(get_disc_service)):
    docs = await service.list_discs()
    return [serialize(d) for d in docs]

@router.get("/{disc_id}", response_model=DiscResponse)
async def get_disc(disc_id: str, service: DiscService = Depends(get_disc_service)):
    doc = await service.get_disc(disc_id)
    return serialize(doc)