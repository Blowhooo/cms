from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi import HTTPException

# 라우터 import
from routers import board, character, party, auth  # auth 라우터 추가!

app = FastAPI(
    title="Party Recruitment API",
    version="1.0.0",
    description="파티 모집 시스템 API - JWT 인증 포함"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영환경에서는 구체적인 도메인으로 변경 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)      # 인증 라우터 (로그인/회원가입)
app.include_router(board.router)     # 게시판 라우터
app.include_router(character.router) # 캐릭터 라우터
app.include_router(party.router)     # 파티 라우터

@app.get("/")
def read_root():
    return {
        "message": "Party Recruitment API",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "redoc": "http://localhost:8000/redoc",
        "endpoints": {
            "auth": "/auth",           # 인증 관련 (로그인/회원가입)
            "board": "/board",         # 게시판
            "characters": "/characters", # 캐릭터 관리
            "parties": "/parties"      # 파티 모집
        },
        "features": [
            "JWT 기반 인증",
            "캐릭터 생성/관리",
            "파티 모집/참가",
            "실시간 채팅",
            "게시판"
        ]
    }

@app.get("/health")
def health_check():
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "message": "Party Recruitment API is running"
    }

# 예외 처리 핸들러 (선택사항)
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "요청한 리소스를 찾을 수 없습니다",
            "path": str(request.url),
            "available_endpoints": [
                "/auth",
                "/board", 
                "/characters",
                "/parties"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "서버 내부 오류가 발생했습니다",
            "message": "관리자에게 문의해주세요"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True  # 개발환경에서 자동 리로드
    )