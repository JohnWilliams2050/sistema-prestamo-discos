from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.mongo_uri, serverSelectionTimeoutMS=3000)
db = client[settings.mongo_db_name]

async def crear_indices() -> None:
    """Táctica: indexar los campos más consultados del catálogo."""
    await db["discos"].create_index("titulo")
    await db["discos"].create_index("artista")
    await db["discos"].create_index("stock_disponible")
    await db["clientes"].create_index("email", unique=True)  # also enforces no duplicate registrations

async def verificar_salud() -> bool:
    """Confirms Mongo is actually reachable, not just that FastAPI is up."""
    try:
        await client.admin.command("ping")
        return True
    except Exception:
        return False