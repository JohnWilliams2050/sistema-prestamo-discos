from bson import ObjectId
from app.core.database import db

class DiscRepository:
    def __init__(self):
        self.collection = db["discs"]

    async def create(self, disc_data: dict) -> dict:
        result = await self.collection.insert_one(disc_data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get(self, disc_id: str) -> dict | None:
        return await self.collection.find_one({"_id": ObjectId(disc_id)})

    async def list_all(self) -> list[dict]:
        return await self.collection.find().to_list(length=100)

    async def decrement_available(self, disc_id: str) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(disc_id)},
            {"$inc": {"available_copies": -1}}
        )