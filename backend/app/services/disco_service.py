from app.repositories.disco_repository import DiscoRepository
from app.schemas.disco import DiscoCreate

class DiscoNoDisponibleError(Exception):
    pass

class DiscoNoEncontradoError(Exception):
    pass

class DiscoService:
    def __init__(self, repo: DiscoRepository):
        self.repo = repo

    async def crear_disco(self, data: DiscoCreate) -> dict:
        doc = data.model_dump()
        doc["stock_disponible"] = doc["stock_total"]
        return await self.repo.crear(doc)

    async def obtener_disco(self, disco_id: str) -> dict:
        disco = await self.repo.obtener(disco_id)
        if not disco:
            raise DiscoNoEncontradoError(disco_id)
        return disco

    async def listar_discos(self) -> list[dict]:
        return await self.repo.listar()