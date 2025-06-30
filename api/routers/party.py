from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/parties",
    tags=["파티 모집"]
)

@router.post("", response_model=schemas.PartyResponse)
def create_party(
    party: schemas.PartyCreate,
    db: Session = Depends(get_db),
    current_user: str = "test_user"
):
    """파티 생성"""
    db_party = models.PartyRecruitment(
        leader_id=current_user,
        **party.dict()
    )
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

@router.get("", response_model=List[schemas.PartyResponse])
def get_parties(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """파티 목록 조회"""
    query = db.query(models.PartyRecruitment)
    
    if status:
        query = query.filter(models.PartyRecruitment.status == status)
    
    parties = query.offset(skip).limit(limit).all()
    return parties

@router.post("/{party_id}/join", response_model=dict)
def join_party(
    party_id: int,
    request: schemas.PartyJoinRequest,
    db: Session = Depends(get_db)
):
    """파티 참가"""
    # 파티 확인
    party = db.query(models.PartyRecruitment).filter(
        models.PartyRecruitment.id == party_id
    ).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # 캐릭터 확인
    character = db.query(models.Character).filter(
        models.Character.id == request.character_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # 이미 참가했는지 확인
    existing_member = db.query(models.PartyMember).filter(
        and_(
            models.PartyMember.party_id == party_id,
            models.PartyMember.character_id == request.character_id
        )
    ).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="Already in party")
    
    # 파티 구성 확인 (1탱 2딜 1힐)
    current_composition = {
        1: party.get_class_count(1),
        2: party.get_class_count(2),
        3: party.get_class_count(3),
    }
    
    max_composition = {1: 1, 2: 2, 3: 1}
    if current_composition[character.class_id] >= max_composition[character.class_id]:
        raise HTTPException(
            status_code=400,
            detail=f"Party already has enough {character.class_name}s"
        )
    
    # 파티 참가
    party_member = models.PartyMember(
        party_id=party_id,
        character_id=request.character_id,
        class_id=character.class_id
    )
    db.add(party_member)
    
    # 파티가 가득 찼는지 확인
    if party.member_count + 1 >= 4:
        party.status = models.PartyStatus.full
    
    db.commit()
    
    return {"message": "Successfully joined party"}

@router.get("/{party_id}", response_model=schemas.PartyResponse)
def get_party(party_id: int, db: Session = Depends(get_db)):
    """특정 파티 상세 조회"""
    party = db.query(models.PartyRecruitment).filter(
        models.PartyRecruitment.id == party_id
    ).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party