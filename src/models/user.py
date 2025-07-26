from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    session_id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
