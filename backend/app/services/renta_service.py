from datetime import date, timedelta
from app.repositories.renta_repository import RentaRepository
from app.repositories.disco_repository import DiscoRepository
from app.repositories.cliente_repository import ClienteRepository
from app.services.disco_service import DiscoNoDisponibleError, DiscoNoEncontradoError
from app.services.cliente_service import ClienteNoEncontradoError, ClienteInactivoError
from app.schemas.renta import RentaCreate

DIAS_PRESTAMO = 14

class RentaService:
    def __init__(self, renta_repo: RentaRepository, disco_repo: DiscoRepository, cliente_repo: ClienteRepository):
        self.renta_repo = renta_repo
        self.disco_repo = disco_repo
        self.cliente_repo = cliente_repo

    async def crear_renta(self, data: RentaCreate) -> dict:
        disco = await self.disco_repo.obtener(data.disco_id)
        if not disco:
            raise DiscoNoEncontradoError(data.disco_id)

        cliente = await self.cliente_repo.obtener(data.cliente_id)
        if not cliente:
            raise ClienteNoEncontradoError(data.cliente_id)
        if cliente["estado"] != "activo":
            raise ClienteInactivoError(data.cliente_id)

        if disco["stock_disponible"] <= 0:
            raise DiscoNoDisponibleError(data.disco_id)

        await self.disco_repo.decrementar_stock(data.disco_id)

        renta_doc = {
            "cliente_id": data.cliente_id,
            "disco_id": data.disco_id,
            "fecha_renta": date.today().isoformat(),
            "fecha_limite_devolucion": (date.today() + timedelta(days=DIAS_PRESTAMO)).isoformat(),
            "fecha_devolucion_real": None,
            "estado": "activa",
        }
        return await self.renta_repo.crear_documento_renta(renta_doc)

    async def listar_rentas(self) -> list[dict]:
        return await self.renta_repo.listar()