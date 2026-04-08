from fastapi import FastAPI

from app.config import get_settings
from app.routes import router

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(router)

