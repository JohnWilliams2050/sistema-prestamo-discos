from bson import ObjectId
from app.core.database import db

class MemberRepository:
    def __init__(self):
        self.collection = db['members']

    async def create(self, member_data: dict) -> dict:
        result = await self.collection.insert_one(member_data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get(self, member_id: str) -> dict | None:
        return await self.collection.find_one({"_id": ObjectId(member_id)})

    async def list_all(self) -> list[dict]:
        return await self.collection.find().to_list(Length=100)
        
    async def get_by_email(self, email: str) -> dict | None:
        return await self.collection.find_one({"email": email})

    async def set_active_status(self, member_id: str, active: bool) -> None:
        await self.collection.update_one(
            {"_id": ObjectId(member_id)},
            {"$set": {"active": active}}
        )