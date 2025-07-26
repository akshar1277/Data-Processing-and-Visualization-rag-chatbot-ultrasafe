from fastapi import APIRouter, HTTPException, Depends, Response
from sqlmodel import Session, select
from passlib.context import CryptContext
from src.models.user import User
from src.db.session import get_session
from src.schemas.auth import AuthLoginRequest, AuthSignupRequest
from fastapi import Cookie

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
def signup(data: AuthSignupRequest, db: Session = Depends(get_session)):

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed = pwd_context.hash(data.password)
    user = User(email=data.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created", "user_id": user.id}


@router.post("/login")
def login(
    data: AuthLoginRequest, response: Response, db: Session = Depends(get_session)
):
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    from uuid import uuid4

    user.session_id = str(uuid4())
    db.add(user)
    db.commit()

    response.set_cookie(
        key="session_id",
        value=user.session_id,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="Lax",
        secure=False,
    )
    return {"message": "Logged in", "session_id": user.session_id}


@router.post("/logout")
def logout(
    response: Response,
    session_id: str = Cookie(default=None),
    db: Session = Depends(get_session),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="No session ID found")

    user = db.exec(select(User).where(User.session_id == session_id)).first()
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid session or already logged out"
        )

    user.session_id = None
    db.add(user)
    db.commit()

    response.delete_cookie(key="session_id")

    return {"message": "Logged out successfully"}
