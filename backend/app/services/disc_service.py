from app.repositories.disc_repository import DiscRepository
from app.schemas.disc import DiscCreate

class DiscUnavailableError(Exception):
    pass

class DiscNotFoundError(Exception):
    pass

class DiscService:
    def __init__(self, repo: DiscRepository):
        self.repo = repo

    async def create_disc(self, data: DiscCreate) -> dict:
        doc = data.model_dump()
        doc["available_copies"] = doc["total_copies"]
        return await self.repo.create(doc)

    async def get_disc(self, disc_id: str) -> dict:
        disc = await self.repo.get(disc_id)
        if not disc:
            raise DiscNotFoundError(disc_id)
        return disc

    async def list_discs(self) -> list[dict]:
        return await self.repo.list_all()