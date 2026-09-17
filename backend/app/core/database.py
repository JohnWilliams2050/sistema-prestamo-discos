from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri) #need to modify this line
db = client[settings.mongo_db_name] #need to modify this line