from fastapi import Depends, HTTPException, status
from auth import verify_token, oauth2_scheme
from schemas import User

# 사용자 인증을 위한 의존성
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user = User(username=payload.get("sub"), email=payload.get("email"), is_admin=payload.get("is_admin", False))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# 관리자 권한 체크 의존성
def check_admin(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    return user
