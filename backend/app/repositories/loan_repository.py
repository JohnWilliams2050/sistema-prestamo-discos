from bson import ObjectId
from app.core.database import db

class LoanRepository:
    def __init__(self):
        self.collection = db["loans"]

    async def create(self, loan_data: dict) -> dict:
        result = await self.collection.insert_one(loan_data)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get(self, loan_id: str) -> dict | None:
        return await self.collection.find_one({"_id": ObjectId(loan_id)})

    async def list_all(self) -> list[dict]:
        return await self.collection.find().to_list(length=100)