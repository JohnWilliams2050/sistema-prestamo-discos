from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api import discs, members, loans
from app.services.disc_service import DiscNotFoundError, DiscUnavailableError
from app.services.member_service import MemberNotFoundError, MemberInactiveError

app = FastAPI(title="Music Disc Loan System")
app.include_router(discs.router)
app.include_router(members.router)
app.include_router(loans.router)

@app.exception_handler(DiscNotFoundError)
async def disc_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Disc not found"})

@app.exception_handler(DiscUnavailableError)
async def disc_unavailable_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": "No copies available"})

@app.exception_handler(MemberNotFoundError)
async def member_not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": "Member not found"})

@app.exception_handler(MemberInactiveError)
async def member_inactive_handler(request, exc):
    return JSONResponse(status_code=403, content={"detail": "Member is not active"})

@app.get("/health")
async def health():
    return {"status": "ok"}