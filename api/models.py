from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import enum

# 기존 테이블들
class AdmMember(Base):
    __tablename__ = "adm_member"
    
    id = Column(String(50), primary_key=True)
    password = Column(String(255), nullable=True)
    nick = Column(String(50), nullable=True)
    
    # Relationships
    characters = relationship("Character", back_populates="owner")
    led_parties = relationship("PartyRecruitment", back_populates="leader")
    chat_messages = relationship("PartyChatMessage", back_populates="user")

class SimplePost(Base):
    __tablename__ = "simple_posts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

# 새로운 테이블들
class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), ForeignKey("adm_member.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    class_id = Column(Integer, nullable=False, index=True)  # 1: 탱커, 2: 딜러, 3: 힐러
    ch_str = Column(Integer, default=1)
    ch_dex = Column(Integer, default=1)
    ch_int = Column(Integer, default=1)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    owner = relationship("AdmMember", back_populates="characters")
    party_memberships = relationship("PartyMember", back_populates="character")
    
    @property
    def class_name(self):
        class_names = {1: "탱커", 2: "딜러", 3: "힐러"}
        return class_names.get(self.class_id, "Unknown")

class PartyStatus(str, enum.Enum):
    recruiting = "recruiting"
    full = "full"
    closed = "closed"

class PartyRecruitment(Base):
    __tablename__ = "party_recruitment"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    leader_id = Column(String(50), ForeignKey("adm_member.id"), nullable=False, index=True)
    status = Column(SQLEnum(PartyStatus), default=PartyStatus.recruiting, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    leader = relationship("AdmMember", back_populates="led_parties")
    members = relationship("PartyMember", back_populates="party", cascade="all, delete-orphan")
    chat_messages = relationship("PartyChatMessage", back_populates="party", cascade="all, delete-orphan")
    
    @property
    def member_count(self):
        return len(self.members)
    
    @property
    def is_full(self):
        return self.member_count >= 4
    
    def get_class_count(self, class_id):
        return sum(1 for member in self.members if member.class_id == class_id)

class PartyMember(Base):
    __tablename__ = "party_members"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    party_id = Column(Integer, ForeignKey("party_recruitment.id"), nullable=False, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False, index=True)
    class_id = Column(Integer, nullable=False)  # 중복 저장으로 빠른 체크
    joined_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    party = relationship("PartyRecruitment", back_populates="members")
    character = relationship("Character", back_populates="party_memberships")

class PartyChatMessage(Base):
    __tablename__ = "party_chat_messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    party_id = Column(Integer, ForeignKey("party_recruitment.id"), nullable=False, index=True)
    user_id = Column(String(50), ForeignKey("adm_member.id"), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Relationships
    party = relationship("PartyRecruitment", back_populates="chat_messages")
    user = relationship("AdmMember", back_populates="chat_messages")