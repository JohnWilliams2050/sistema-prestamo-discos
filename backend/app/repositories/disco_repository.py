from bson import ObjectId
from app.core.database import db
from app.core.resiliencia import con_reintentos

class DiscoRepository:
    def __init__(self):
        self.collection = db["discos"]

    async def crear(self, disco_data: dict) -> dict:
        result = await con_reintentos(self.collection.insert_one, disco_data)
        return await con_reintentos(self.collection.find_one, {"_id": result.inserted_id})

    async def obtener(self, disco_id: str) -> dict | None:
        return await con_reintentos(self.collection.find_one, {"_id": ObjectId(disco_id)})

    async def listar(self) -> list[dict]:
        return await con_reintentos(self.collection.find().to_list, length=100)

    async def decrementar_stock(self, disco_id: str) -> None:
        await con_reintentos(self.collection.update_one, {"_id": ObjectId(disco_id)}, {"$inc": {"stock_disponible": -1}})