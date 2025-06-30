from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

# 라우터 생성
router = APIRouter(
    prefix="/board",
    tags=["게시판"]
)

@router.post("", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """게시글 작성"""
    db_post = models.SimplePost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("", response_model=List[schemas.PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """게시글 목록 조회"""
    posts = db.query(models.SimplePost).offset(skip).limit(limit).all()
    return posts