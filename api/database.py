from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 환경변수에서 DB URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL")

# 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 개발 중에는 SQL 로그 출력
    pool_pre_ping=True,  # 연결 상태 확인
)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()