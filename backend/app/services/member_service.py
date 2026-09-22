from app.repositories.member_repository import MemberRepository
from app.schemas.member import MemberCreate

class MemberNotFoundError(Exception):
    pass

class MemberInactiveError(Exception):
    pass

class MemberService:
    def __init__(self, repo: MemberRepository):
        self.repo = repo

    async def create_member(self, data: MemberCreate) -> dict:
        doc = data.model_dump()
        doc["active"] = True
        return await self.repo.create(doc)

    async def get_member(self, member_id: str) -> dict:
        member = await self.repo.get(member_id)
        if not member:
            raise MemberNotFoundError(member_id)
        return member

    async def list_members(self) -> list[dict]:
        return await self.repo.list_all()

    async def deactivate_member(self, member_id: str) -> dict:
        await self.get_member(member_id)  # raises MemberNotFoundError if missing
        await self.repo.set_active_status(member_id, False)
        return await self.repo.get(member_id)

    async def activate_member(self, member_id: str) -> dict:
        await self.get_member(member_id)
        await self.repo.set_active_status(member_id, True)
        return await self.repo.get(member_id)

    async def find_by_email(self, email: str) -> dict | None:
        return await self.repo.get_by_email(email)