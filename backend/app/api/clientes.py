from fastapi import APIRouter, Depends
from app.schemas.cliente import ClienteCreate
from app.services.cliente_service import ClienteService, ClienteNoEncontradoError
from app.repositories.cliente_repository import ClienteRepository
from app.core.jsonapi import JSONAPIResponse, single, collection

router = APIRouter(prefix="/clientes", tags=["clientes"], default_response_class=JSONAPIResponse)

def get_cliente_service() -> ClienteService:
    return ClienteService(ClienteRepository())

def attrs(doc: dict) -> dict:
    return {k: v for k, v in doc.items() if k != "_id"}

@router.post("/", status_code=201)
async def crear_cliente(data: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    doc = await service.crear_cliente(data)
    return single("clientes", str(doc["_id"]), attrs(doc))

@router.get("/buscar")
async def buscar_cliente(email: str, service: ClienteService = Depends(get_cliente_service)):
    cliente = await service.buscar_por_email(email)
    if not cliente:
        raise ClienteNoEncontradoError(email)
    return single("clientes", str(cliente["_id"]), attrs(cliente))

@router.get("/{cliente_id}")
async def obtener_cliente(cliente_id: str, service: ClienteService = Depends(get_cliente_service)):
    doc = await service.obtener_cliente(cliente_id)
    return single("clientes", str(doc["_id"]), attrs(doc))

@router.patch("/{cliente_id}/desactivar")
async def desactivar_cliente(cliente_id: str, service: ClienteService = Depends(get_cliente_service)):
    doc = await service.desactivar_cliente(cliente_id)
    return single("clientes", str(doc["_id"]), attrs(doc))

@router.patch("/{cliente_id}/activar")
async def activar_cliente(cliente_id: str, service: ClienteService = Depends(get_cliente_service)):
    doc = await service.activar_cliente(cliente_id)
    return single("clientes", str(doc["_id"]), attrs(doc))