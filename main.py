from fastapi import FastAPI
from src.api.routes import router as upload_router
from src.api.auth import router as auth_router
from src.middleware.session_middleware import SessionMiddleware
from src.config.langfuse import langfuse

app = FastAPI()


app.include_router(auth_router)
app.include_router(upload_router)
app.add_middleware(SessionMiddleware)
