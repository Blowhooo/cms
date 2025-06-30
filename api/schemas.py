from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, validator  # validator 추가!

# 기존 게시글 스키마
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True

# 캐릭터 스키마
class CharacterBase(BaseModel):
    name: str
    class_id: int
    ch_str:int
    ch_dex:int
    ch_int:int
    
    @validator('class_id')
    def validate_class_id(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('class_id must be 1 (탱커), 2 (딜러), or 3 (힐러)')
        return v

class CharacterCreate(CharacterBase):
    pass

class CharacterResponse(CharacterBase):
    id: int
    user_id: str
    level: int
    created_at: datetime
    class_name: str
    ch_str:int
    ch_dex:int
    ch_int:int
    
    class Config:
        orm_mode = True

# 파티 스키마
class PartyStatus(str, Enum):
    recruiting = "recruiting"
    full = "full"
    closed = "closed"

class PartyCreate(BaseModel):
    title: str
    description: Optional[str] = None

class PartyMemberInfo(BaseModel):
    character_id: int
    character_name: str
    class_id: int
    class_name: str
    joined_at: datetime
    
    class Config:
        orm_mode = True

class PartyMemberInfo(BaseModel):
    character_id: int
    character_name: str
    class_id: int
    class_name: str
    joined_at: datetime
    
    @classmethod
    def from_party_member(cls, party_member):
        """PartyMember 객체로부터 생성"""
        return cls(
            character_id=party_member.character.id,
            character_name=party_member.character.name,
            class_id=party_member.character.class_id,
            class_name=party_member.character.class_name,
            joined_at=party_member.joined_at
        )
    
    class Config:
        orm_mode = True

class PartyResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    leader_id: str
    status: PartyStatus
    created_at: datetime
    member_count: int
    members: List[PartyMemberInfo] = []
    
    @validator('members', pre=True)
    def convert_members(cls, v):
        """PartyMember 객체들을 PartyMemberInfo로 변환"""
        if v and hasattr(v[0], 'character'):
            return [PartyMemberInfo.from_party_member(member) for member in v]
        return v
    
    class Config:
        orm_mode = True

class PartyJoinRequest(BaseModel):
    character_id: int