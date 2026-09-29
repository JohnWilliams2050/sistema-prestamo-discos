from fastapi import APIRouter, Depends
from app.schemas.renta import RentaCreate, RentaResponse
from app.services.renta_service import RentaService
from app.repositories.renta_repository import RentaRepository
from app.repositories.disco_repository import DiscoRepository
from app.repositories.cliente_repository import ClienteRepository
from app.core.jsonapi import JSONAPIResponse, single, collection, relationship

router = APIRouter(prefix="/rentas", tags=["rentas"], default_response_class=JSONAPIResponse)

def get_renta_service() -> RentaService:
    return RentaService(RentaRepository(), DiscoRepository(), ClienteRepository())

def attrs(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k not in ("_id", "cliente_id", "disco_id")}

def rels(doc: dict) -> dict:
    return {
        "cliente": relationship("clientes", doc["cliente_id"]),
        "disco": relationship("discos", doc["disco_id"]),
    }

@router.post("/", status_code=201)
async def crear_renta(data: RentaCreate, service: RentaService = Depends(get_renta_service)):
    doc = await service.crear_renta(data)
    return single("rentas", str(doc["_id"]), attrs(doc), rels(doc))

@router.get("/")
async def listar_rentas(service: RentaService = Depends(get_renta_service)):
    docs = await service.listar_rentas()
    return collection("rentas", [(str(d["_id"]), attrs(d), rels(d)) for d in docs])