from fastapi import APIRouter, Depends
from app.schemas.disco import DiscoCreate, DiscoResponse
from app.services.disco_service import DiscoService
from app.repositories.disco_repository import DiscoRepository
from app.core.jsonapi import JSONAPIResponse, single, collection

router = APIRouter(prefix="/discos", tags=["discos"], default_response_class=JSONAPIResponse)

def get_disco_service() -> DiscoService:
    return DiscoService(DiscoRepository())

def attrs(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k != "_id"}

@router.post("/", status_code=201)
async def crear_disco(data: DiscoCreate, service: DiscoService = Depends(get_disco_service)):
    doc = await service.crear_disco(data)
    return single("discos", str(doc["_id"]), attrs(doc))

@router.get("/", status_code=200)
async def listar_discos(service: DiscoService = Depends(get_disco_service)):
    docs = await service.listar_discos()
    return collection("discos", [(str(d["_id"]), attrs(d), None) for d in docs])

@router.get("/{disco_id}", response_model=DiscoResponse)
async def obtener_disco(disco_id: str, service: DiscoService = Depends(get_disco_service)):
    doc = await service.obtener_disco(disco_id)
    return single("discos", str(doc["_id"]), attrs(doc))