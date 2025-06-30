from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 라우터 import
from routers import board, character, party

app = FastAPI(
    title="Party Recruitment API",
    version="1.0.0",
    description="파티 모집 시스템 API"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(board.router)
app.include_router(character.router)
app.include_router(party.router)

@app.get("/")
def read_root():
    return {
        "message": "Party Recruitment API",
        "docs": "http://localhost:8000/docs",
        "endpoints": {
            "board": "/board",
            "characters": "/characters",
            "parties": "/parties"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)