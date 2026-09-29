from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate

class ClienteNoEncontradoError(Exception):
    pass

class ClienteInactivoError(Exception):
    pass

class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    async def crear_cliente(self, data: ClienteCreate) -> dict:
        doc = data.model_dump()
        doc["estado"] = "activo"
        return await self.repo.crear(doc)

    async def obtener_cliente(self, cliente_id: str) -> dict:
        cliente = await self.repo.obtener(cliente_id)
        if not cliente:
            raise ClienteNoEncontradoError(cliente_id)
        return cliente

    async def buscar_por_email(self, email: str) -> dict | None:
        return await self.repo.obtener_por_email(email)

    async def desactivar_cliente(self, cliente_id: str) -> dict:
        await self.obtener_cliente(cliente_id)
        await self.repo.actualizar_estado(cliente_id, "inactivo")
        return await self.repo.obtener(cliente_id)

    async def activar_cliente(self, cliente_id: str) -> dict:
        await self.obtener_cliente(cliente_id)
        await self.repo.actualizar_estado(cliente_id, "activo")
        return await self.repo.obtener(cliente_id)