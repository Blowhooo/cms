from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

# DB 접속 정보 (XAMPP 기준, 비밀번호는 실제 사용 중인 값으로 수정)
# DB_URL = "mysql+pymysql://fastapi_user:Tjdtj%21%210714@210.114.17.9:3306/wan"  # 비밀번호 없으면 그냥 공란
DB_URL = "mysql+pymysql://cybershock:tjdtj!!0714@cybershock.mycafe24.com:3306/cybershock"  # 비밀번호 없으면 그냥 공란

engine = create_engine(DB_URL, echo=True)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PostCreate(BaseModel):
    title: str
    content: str

# 게시글 등록 API
@app.post("/board")
def create_post(post: PostCreate):
    try:
        with engine.begin() as conn:
            sql = text("""
                INSERT INTO simple_posts (title, content)
                VALUES (:title, :content)
            """)
            conn.execute(sql, {
                "title": post.title,
                "content": post.content
            })
        return { "success": True }
    except Exception as e:
        print("DB Error:", e)
        raise HTTPException(status_code=500, detail="서버 내부 오류")


@app.get("/test-db")
async def test_database():
    try:
        # 여기에 실제 DB 연결 코드
        # 예: SQLAlchemy 사용 시
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"status": "DB 연결 성공!", "result": result.scalar()}
    except Exception as e:
        return {"status": "DB 연결 실패", "error": str(e), "type": type(e).__name__}