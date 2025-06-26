from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from fastapi import HTTPException

# DB 접속 정보 (XAMPP 기준, 비밀번호는 실제 사용 중인 값으로 수정)
# DB_URL = "mysql+pymysql://fastapi_user:Tjdtj%21%210714@210.114.17.9:3306/wan"  # 비밀번호 없으면 그냥 공란
DB_URL = "mysql+pymysql://cybershock:tjdtj!!0714@cybershock.mycafe24.com:3306/cybershock"  # 비밀번호 없으면 그냥 공란

engine = create_engine(DB_URL, echo=True)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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