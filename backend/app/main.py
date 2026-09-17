from fastapi import FastAPI

app = FastAPI(title="Music Disc Loan System")

@app.get("/health")
async def health():
    return {"status": "ok"}