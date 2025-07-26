from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlmodel import Session as DBSession, select
from src.db.session import engine
from src.models.user import User


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get("session_id")
        user = None

        if session_id:
            with DBSession(engine) as db:
                user = db.exec(
                    select(User).where(User.session_id == session_id)
                ).first()

        request.state.user = user
        response = await call_next(request)
        return response
