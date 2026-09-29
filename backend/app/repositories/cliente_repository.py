from bson import ObjectId
from app.core.database import db
from app.core.resiliencia import con_reintentos

class ClienteRepository:
    def __init__(self):
        self.collection = db["clientes"]

    async def crear(self, cliente_data: dict) -> dict:
        result = await con_reintentos(self.collection.insert_one, cliente_data)
        return await con_reintentos(self.collection.find_one, {"_id": result.inserted_id})

    async def obtener(self, cliente_id: str) -> dict | None:
        return await con_reintentos(self.collection.find_one, {"_id": ObjectId(cliente_id)})

    async def obtener_por_email(self, email: str) -> dict | None:
        return await con_reintentos(self.collection.find_one, {"email": email})

    async def actualizar_estado(self, cliente_id: str, estado: str) -> None:
        await con_reintentos(self.collection.update_one, {"_id": ObjectId(cliente_id)}, {"$set": {"estado": estado}})