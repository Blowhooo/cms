# login.py - 로그인 관련 기능 모듈
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional
import os
from database import get_db
from models import AdmMember

# 환경변수에서 설정값 가져오기 (없으면 기본값 사용)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 패스워드 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 토큰 인증 설정
security = HTTPBearer()

class LoginManager:
    """로그인 관리 클래스"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        비밀번호 검증
        
        Args:
            plain_password: 평문 비밀번호
            hashed_password: 해싱된 비밀번호
            
        Returns:
            bool: 비밀번호 일치 여부
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        비밀번호 해싱
        
        Args:
            password: 평문 비밀번호
            
        Returns:
            str: 해싱된 비밀번호
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def get_user(db: Session, user_id: str) -> Optional[AdmMember]:
        """
        사용자 조회
        
        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID
            
        Returns:
            AdmMember: 사용자 객체 (없으면 None)
        """
        return db.query(AdmMember).filter(AdmMember.id == user_id).first()
    
    @staticmethod
    def authenticate_user(db: Session, user_id: str, password: str) -> Optional[AdmMember]:
        """
        사용자 인증
        
        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID
            password: 평문 비밀번호
            
        Returns:
            AdmMember: 인증된 사용자 객체 (실패시 None)
        """
        user = LoginManager.get_user(db, user_id)
        if not user:
            return None
        if not user.password:  # 비밀번호가 설정되지 않은 경우
            return None
        if not LoginManager.verify_password(password, user.password):
            return None
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        JWT 액세스 토큰 생성
        
        Args:
            data: 토큰에 포함할 데이터
            expires_delta: 토큰 만료 시간 (없으면 기본값 사용)
            
        Returns:
            str: JWT 토큰
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),  # 토큰 발급 시간
            "type": "access_token"
        })
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        JWT 토큰 검증
        
        Args:
            token: JWT 토큰
            
        Returns:
            dict: 토큰 페이로드
            
        Raises:
            HTTPException: 토큰이 유효하지 않은 경우
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return payload
        except JWTError as e:
            print(f"JWT Error: {e}")  # 로그용
            raise credentials_exception
    
    @staticmethod
    def create_user(db: Session, user_id: str, password: str, nick: str) -> AdmMember:
        """
        새 사용자 생성
        
        Args:
            db: 데이터베이스 세션
            user_id: 사용자 ID
            password: 평문 비밀번호
            nick: 닉네임
            
        Returns:
            AdmMember: 생성된 사용자 객체
            
        Raises:
            HTTPException: 사용자 ID가 이미 존재하는 경우
        """
        # 중복 확인
        existing_user = LoginManager.get_user(db, user_id)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 사용자 ID입니다"
            )
        
        # 비밀번호 해싱
        hashed_password = LoginManager.get_password_hash(password)
        
        # 새 사용자 생성
        new_user = AdmMember(
            id=user_id,
            password=hashed_password,
            nick=nick
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def change_password(db: Session, user: AdmMember, old_password: str, new_password: str) -> bool:
        """
        비밀번호 변경
        
        Args:
            db: 데이터베이스 세션
            user: 사용자 객체
            old_password: 기존 비밀번호
            new_password: 새 비밀번호
            
        Returns:
            bool: 변경 성공 여부
        """
        # 기존 비밀번호 확인
        if not LoginManager.verify_password(old_password, user.password):
            return False
        
        # 새 비밀번호로 변경
        user.password = LoginManager.get_password_hash(new_password)
        db.commit()
        
        return True

# Dependency 함수들
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> AdmMember:
    """
    현재 사용자 인증 및 조회 (FastAPI Dependency)
    
    Args:
        credentials: HTTP Bearer 토큰
        db: 데이터베이스 세션
        
    Returns:
        AdmMember: 현재 인증된 사용자
        
    Raises:
        HTTPException: 인증 실패시
    """
    # 토큰 검증
    payload = LoginManager.verify_token(credentials.credentials)
    user_id = payload.get("sub")
    
    # 사용자 조회
    user = LoginManager.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_active_user(
    current_user: AdmMember = Depends(get_current_user)
) -> AdmMember:
    """
    활성 사용자 확인 (추후 is_active 필드 추가시 사용)
    
    Args:
        current_user: 현재 사용자
        
    Returns:
        AdmMember: 활성 사용자
        
    Raises:
        HTTPException: 비활성 사용자인 경우
    """
    # 현재는 모든 사용자가 활성 상태로 간주
    # 추후 AdmMember에 is_active 필드 추가시 검증 로직 추가
    return current_user

# 선택적: 관리자 권한 확인 (추후 role 필드 추가시)
async def get_admin_user(
    current_user: AdmMember = Depends(get_current_active_user)
) -> AdmMember:
    """
    관리자 권한 확인 (추후 구현)
    
    Args:
        current_user: 현재 사용자
        
    Returns:
        AdmMember: 관리자 사용자
        
    Raises:
        HTTPException: 관리자가 아닌 경우
    """
    # 추후 AdmMember에 role 필드 추가시 구현
    # if not current_user.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="관리자 권한이 필요합니다"
    #     )
    return current_user

# 유틸리티 함수들
def validate_password_strength(password: str) -> bool:
    """
    비밀번호 강도 검증
    
    Args:
        password: 검증할 비밀번호
        
    Returns:
        bool: 강도 요구사항 만족 여부
    """
    if len(password) < 8:
        return False
    
    # 영문, 숫자 포함 확인
    has_alpha = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    return has_alpha and has_digit

def generate_temporary_password(length: int = 12) -> str:
    """
    임시 비밀번호 생성
    
    Args:
        length: 비밀번호 길이
        
    Returns:
        str: 임시 비밀번호
    """
    import random
    import string
    
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# 로그인 매니저 인스턴스 (전역 사용)
login_manager = LoginManager()