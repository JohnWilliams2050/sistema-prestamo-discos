from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import discos, clientes, rentas
from app.services.disco_service import DiscoNoEncontradoError, DiscoNoDisponibleError
from app.services.cliente_service import ClienteNoEncontradoError, ClienteInactivoError
from app.core.database import crear_indices
from app.core.jsonapi import JSONAPIResponse, errors

@asynccontextmanager
async def lifespan(app: FastAPI):
    await crear_indices()
    yield

app = FastAPI(title="Sistema de Renta de Discos", lifespan=lifespan, default_response_class=JSONAPIResponse)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(discos.router)
app.include_router(clientes.router)
app.include_router(rentas.router)

@app.exception_handler(DiscoNoEncontradoError)
async def disco_no_encontrado_handler(request, exc):
    return JSONAPIResponse(status_code=404, content=errors(404, "Disco no encontrado", str(exc)))

@app.exception_handler(DiscoNoDisponibleError)
async def disco_no_disponible_handler(request, exc):
    return JSONAPIResponse(status_code=409, content=errors(409, "Sin stock disponible", "El disco no tiene copias disponibles"))

@app.exception_handler(ClienteNoEncontradoError)
async def cliente_no_encontrado_handler(request, exc):
    return JSONAPIResponse(status_code=404, content=errors(404, "Cliente no encontrado", str(exc)))

@app.exception_handler(ClienteInactivoError)
async def cliente_inactivo_handler(request, exc):
    return JSONAPIResponse(status_code=403, content=errors(403, "Cliente inactivo", "El cliente no está activo"))

@app.get("/health")
async def health():
    return {"status": "ok"}