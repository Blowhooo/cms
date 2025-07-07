from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

# ==================== 인증 관련 스키마 ====================

class UserLogin(BaseModel):
    """로그인 요청 스키마"""
    id: str = Field(..., min_length=3, max_length=50, description="사용자 ID")
    password: str = Field(..., min_length=1, description="비밀번호")

class UserCreate(BaseModel):
    """회원가입 요청 스키마"""
    id: str = Field(..., min_length=3, max_length=50, description="사용자 ID")
    password: str = Field(..., min_length=8, max_length=100, description="비밀번호")
    nick: str = Field(..., min_length=2, max_length=50, description="닉네임")
    
    @validator('id')
    def validate_user_id(cls, v):
        """사용자 ID 검증"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('사용자 ID는 영문, 숫자, _, - 만 사용 가능합니다')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        """비밀번호 강도 검증"""
        if len(v) < 8:
            raise ValueError('비밀번호는 8자 이상이어야 합니다')
        
        has_alpha = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_alpha and has_digit):
            raise ValueError('비밀번호는 영문과 숫자를 포함해야 합니다')
        
        return v

class PasswordChange(BaseModel):
    """비밀번호 변경 요청 스키마"""
    old_password: str = Field(..., description="기존 비밀번호")
    new_password: str = Field(..., min_length=8, max_length=100, description="새 비밀번호")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """새 비밀번호 강도 검증"""
        if len(v) < 8:
            raise ValueError('비밀번호는 8자 이상이어야 합니다')
        
        has_alpha = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_alpha and has_digit):
            raise ValueError('비밀번호는 영문과 숫자를 포함해야 합니다')
        
        return v

class Token(BaseModel):
    """JWT 토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = 1800  # 30분 (초 단위)

class UserResponse(BaseModel):
    """사용자 정보 응답 스키마"""
    id: str
    nick: str
    
    class Config:
        from_attributes = True  # Pydantic v2 방식

# ==================== 기존 게시글 스키마 ====================

class PostCreate(BaseModel):
    """게시글 생성 요청 스키마"""
    title: str = Field(..., min_length=1, max_length=255, description="제목")
    content: str = Field(..., min_length=1, description="내용")

class PostResponse(BaseModel):
    """게시글 응답 스키마"""
    id: int
    title: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== 캐릭터 스키마 ====================

class CharacterBase(BaseModel):
    """캐릭터 기본 스키마"""
    name: str = Field(..., min_length=2, max_length=50, description="캐릭터 이름")
    class_id: int = Field(..., ge=1, le=3, description="직업 ID (1: 탱커, 2: 딜러, 3: 힐러)")
    
    @validator('class_id')
    def validate_class_id(cls, v):
        if v not in [1, 2, 3]:
            raise ValueError('class_id must be 1 (탱커), 2 (딜러), or 3 (힐러)')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('캐릭터 이름은 공백일 수 없습니다')
        return v.strip()

class CharacterCreate(CharacterBase):
    """캐릭터 생성 요청 스키마"""
    ch_str: Optional[int] = Field(default=1, ge=1, le=999, description="힘")
    ch_dex: Optional[int] = Field(default=1, ge=1, le=999, description="민첩")
    ch_int: Optional[int] = Field(default=1, ge=1, le=999, description="지능")

class CharacterUpdate(BaseModel):
    """캐릭터 업데이트 스키마"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    ch_str: Optional[int] = Field(None, ge=1, le=999)
    ch_dex: Optional[int] = Field(None, ge=1, le=999)
    ch_int: Optional[int] = Field(None, ge=1, le=999)

class CharacterResponse(CharacterBase):
    """캐릭터 응답 스키마"""
    id: int
    user_id: str
    level: int
    ch_str: int
    ch_dex: int
    ch_int: int
    created_at: datetime
    class_name: str
    
    class Config:
        from_attributes = True

# ==================== 파티 스키마 ====================

class PartyStatus(str, Enum):
    """파티 상태 열거형"""
    recruiting = "recruiting"
    full = "full"
    closed = "closed"

class PartyCreate(BaseModel):
    """파티 생성 요청 스키마"""
    title: str = Field(..., min_length=1, max_length=255, description="파티 제목")
    description: Optional[str] = Field(None, max_length=1000, description="파티 설명")

class PartyUpdate(BaseModel):
    """파티 수정 요청 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[PartyStatus] = None

class PartyMemberInfo(BaseModel):
    """파티 멤버 정보 스키마"""
    character_id: int
    character_name: str
    class_id: int
    class_name: str
    joined_at: datetime
    level: int = 1  # 캐릭터 레벨 추가
    
    @classmethod
    def from_party_member(cls, party_member):
        """PartyMember 객체로부터 생성"""
        return cls(
            character_id=party_member.character.id,
            character_name=party_member.character.name,
            class_id=party_member.character.class_id,
            class_name=party_member.character.class_name,
            level=party_member.character.level,
            joined_at=party_member.joined_at
        )
    
    class Config:
        from_attributes = True

class PartyResponse(BaseModel):
    """파티 응답 스키마"""
    id: int
    title: str
    description: Optional[str]
    leader_id: str
    leader_nick: Optional[str] = None  # 리더 닉네임 추가
    status: PartyStatus
    created_at: datetime
    updated_at: datetime
    member_count: int
    max_members: int = 4  # 최대 멤버 수
    members: List[PartyMemberInfo] = []
    
    # 직업별 인원 수 정보 추가
    tank_count: int = 0
    dealer_count: int = 0
    healer_count: int = 0
    
    @validator('members', pre=True)
    def convert_members(cls, v):
        """PartyMember 객체들을 PartyMemberInfo로 변환"""
        if v and hasattr(v[0], 'character'):
            return [PartyMemberInfo.from_party_member(member) for member in v]
        return v
    
    @validator('tank_count', pre=True, always=True)
    def set_tank_count(cls, v, values):
        """탱커 수 계산"""
        members = values.get('members', [])
        return sum(1 for member in members if member.class_id == 1)
    
    @validator('dealer_count', pre=True, always=True)
    def set_dealer_count(cls, v, values):
        """딜러 수 계산"""
        members = values.get('members', [])
        return sum(1 for member in members if member.class_id == 2)
    
    @validator('healer_count', pre=True, always=True)
    def set_healer_count(cls, v, values):
        """힐러 수 계산"""
        members = values.get('members', [])
        return sum(1 for member in members if member.class_id == 3)
    
    class Config:
        from_attributes = True

class PartyJoinRequest(BaseModel):
    """파티 참가 요청 스키마"""
    character_id: int = Field(..., gt=0, description="참가할 캐릭터 ID")

class PartyListResponse(BaseModel):
    """파티 목록 응답 스키마"""
    id: int
    title: str
    leader_nick: str
    status: PartyStatus
    member_count: int
    max_members: int = 4
    tank_count: int
    dealer_count: int
    healer_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== 채팅 스키마 ====================

class ChatMessageCreate(BaseModel):
    """채팅 메시지 생성 스키마"""
    message: str = Field(..., min_length=1, max_length=1000, description="메시지 내용")
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('메시지는 공백일 수 없습니다')
        return v.strip()

class ChatMessageResponse(BaseModel):
    """채팅 메시지 응답 스키마"""
    id: int
    party_id: int
    user_id: str
    user_nick: str  # 사용자 닉네임 추가
    message: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ==================== 사용자 확장 스키마 ====================

class UserWithCharacters(UserResponse):
    """캐릭터 정보를 포함한 사용자 응답 스키마"""
    characters: List[CharacterResponse] = []

class UserStats(BaseModel):
    """사용자 통계 스키마"""
    total_characters: int
    total_parties_led: int
    total_parties_joined: int
    
    class Config:
        from_attributes = True

# ==================== 공통 응답 스키마 ====================

class MessageResponse(BaseModel):
    """일반 메시지 응답 스키마"""
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    detail: str
    error_code: Optional[str] = None

# ==================== 페이지네이션 스키마 ====================

class PaginationParams(BaseModel):
    """페이지네이션 파라미터 스키마"""
    page: int = Field(default=1, ge=1, description="페이지 번호")
    size: int = Field(default=20, ge=1, le=100, description="페이지 크기")

class PaginatedResponse(BaseModel):
    """페이지네이션 응답 스키마"""
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int
    
    @validator('pages', pre=True, always=True)
    def calculate_pages(cls, v, values):
        """총 페이지 수 계산"""
        total = values.get('total', 0)
        size = values.get('size', 20)
        return (total + size - 1) // size if total > 0 else 1