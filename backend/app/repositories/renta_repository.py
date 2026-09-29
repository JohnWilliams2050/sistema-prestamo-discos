from bson import ObjectId
from app.core.database import db
from app.core.resiliencia import con_reintentos

class RentaRepository:
    def __init__(self):
        self.collection = db["rentas"]

    async def crear_documento_renta(self, renta_data: dict) -> dict:
        result = await con_reintentos(self.collection.insert_one, renta_data)
        return await con_reintentos(self.collection.find_one, {"_id": result.inserted_id})

    async def listar(self) -> list[dict]:
        return await con_reintentos(self.collection.find().to_list(length=100))