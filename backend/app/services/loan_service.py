from datetime import date, timedelta
from app.repositories.loan_repository import LoanRepository
from app.repositories.disc_repository import DiscRepository
from app.repositories.member_repository import MemberRepository
from app.services.disc_service import DiscUnavailableError, DiscNotFoundError
from app.services.member_service import MemberNotFoundError, MemberInactiveError
from app.schemas.loan import LoanCreate

LOAN_PERIOD_DAYS = 14

class LoanService:
    def __init__(self, loan_repo: LoanRepository, disc_repo: DiscRepository, member_repo: MemberRepository):
        self.loan_repo = loan_repo
        self.disc_repo = disc_repo
        self.member_repo = member_repo

    async def create_loan(self, data: LoanCreate) -> dict:
        disc = await self.disc_repo.get(data.disc_id)
        if not disc:
            raise DiscNotFoundError(data.disc_id)

        member = await self.member_repo.get(data.member_id)
        if not member:
            raise MemberNotFoundError(data.member_id)

        if not member["active"]:
            raise MemberInactiveError(data.member_id)

        if disc["available_copies"] <= 0:
            raise DiscUnavailableError(data.disc_id)

        await self.disc_repo.decrement_available(data.disc_id)

        loan_doc = {
            "disc_id": data.disc_id,
            "member_id": data.member_id,
            "loan_date": date.today().isoformat(),
            "due_date": (date.today() + timedelta(days=LOAN_PERIOD_DAYS)).isoformat(),
            "returned": False,
        }
        return await self.loan_repo.create(loan_doc)

    async def list_loans(self) -> list[dict]:
        return await self.loan_repo.list_all()