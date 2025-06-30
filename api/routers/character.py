from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/characters",
    tags=["캐릭터"]
)

@router.post("", response_model=schemas.CharacterResponse)
def create_character(
    character: schemas.CharacterCreate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"  # 나중에 인증 추가
):
    """캐릭터 생성"""
    db_character = models.Character(
        user_id=current_user,
        **character.dict()
    )
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

@router.get("", response_model=List[schemas.CharacterResponse])
def get_my_characters(
    db: Session = Depends(get_db),
    current_user: str = "test_user"
):
    """내 캐릭터 목록 조회"""
    characters = db.query(models.Character).filter(
        models.Character.user_id == current_user
    ).all()
    return characters