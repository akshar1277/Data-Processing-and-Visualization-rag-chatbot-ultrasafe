from sqlmodel import SQLModel
from src.models.user import User
from src.db.session import engine

def init_db():
    SQLModel.metadata.create_all(engine)
    print("✅ Database initialized")

if __name__ == "__main__":
    init_db()
