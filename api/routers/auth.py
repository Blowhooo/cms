# routers/auth.py - 인증 관련 라우터
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from login import LoginManager, get_current_user, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import (
    UserLogin, 
    UserCreate, 
    PasswordChange,
    Token, 
    UserResponse, 
    UserWithCharacters,
    MessageResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["인증"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"}
    }
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    회원가입
    
    - **id**: 사용자 ID (3-50자, 영문/숫자/_/- 만 허용)
    - **password**: 비밀번호 (8자 이상, 영문+숫자 필수)
    - **nick**: 닉네임 (2-50자)
    """
    try:
        new_user = LoginManager.create_user(
            db=db,
            user_id=user.id,
            password=user.password,
            nick=user.nick
        )
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        print(f"회원가입 에러: {e}")  # 👈 이 줄 추가!
        print(f"에러 타입: {type(e)}")  # 👈 이 줄도 추가!
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"회원가입 중 오류가 발생했습니다: {str(e)}"  # 👈 실제 에러 메시지 포함
        )

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    로그인
    
    - **id**: 사용자 ID
    - **password**: 비밀번호
    
    성공시 JWT 액세스 토큰을 반환합니다.
    """
    authenticated_user = LoginManager.authenticate_user(
        db, user.id, user.password
    )
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자 ID 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = LoginManager.create_access_token(
        data={"sub": authenticated_user.id}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 초 단위
    }

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    """
    내 정보 조회
    
    인증된 사용자의 기본 정보를 반환합니다.
    """
    return current_user

@router.get("/me/detail", response_model=UserWithCharacters)
async def get_me_with_characters(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    내 상세 정보 조회 (캐릭터 포함)
    
    인증된 사용자의 정보와 보유한 캐릭터 목록을 함께 반환합니다.
    """
    # 사용자의 캐릭터들을 함께 로드
    from models import AdmMember
    user_with_characters = db.query(AdmMember).filter(
        AdmMember.id == current_user.id
    ).first()
    
    return user_with_characters

@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    비밀번호 변경
    
    - **old_password**: 현재 비밀번호
    - **new_password**: 새 비밀번호 (8자 이상, 영문+숫자 필수)
    """
    success = LoginManager.change_password(
        db, current_user, password_data.old_password, password_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="현재 비밀번호가 올바르지 않습니다"
        )
    
    return {
        "message": "비밀번호가 성공적으로 변경되었습니다",
        "success": True
    }

@router.post("/logout", response_model=MessageResponse)
async def logout(current_user = Depends(get_current_user)):
    """
    로그아웃
    
    현재는 클라이언트에서 토큰을 삭제하도록 안내합니다.
    추후 토큰 블랙리스트 기능을 추가할 수 있습니다.
    """
    return {
        "message": "로그아웃되었습니다. 클라이언트에서 토큰을 삭제해주세요.",
        "success": True
    }

@router.get("/check-id/{user_id}")
async def check_user_id_availability(user_id: str, db: Session = Depends(get_db)):
    """
    사용자 ID 중복 확인
    
    회원가입 전에 사용자 ID가 이미 사용중인지 확인합니다.
    """
    existing_user = LoginManager.get_user(db, user_id)
    if existing_user:
        return {
            "available": False,
            "message": "이미 사용중인 ID입니다"
        }
    return {
        "available": True,
        "message": "사용 가능한 ID입니다"
    }

@router.get("/verify-token")
async def verify_token(current_user = Depends(get_current_user)):
    """
    토큰 검증
    
    현재 토큰이 유효한지 확인합니다.
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "nick": current_user.nick,
        "message": "토큰이 유효합니다"
    }

# 관리자 전용 엔드포인트 (추후 구현)
@router.get("/admin/users", dependencies=[Depends(get_current_active_user)])
async def list_users_admin():
    """
    사용자 목록 조회 (관리자용)
    
    추후 관리자 권한 확인 기능과 함께 구현 예정
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="관리자 기능은 추후 구현 예정입니다"
    )