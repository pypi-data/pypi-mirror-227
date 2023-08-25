from ...main import AppProject
from ..config import NameConfig
from .base import (
    SimpleModuleCode,
)


class MainModuleCode(SimpleModuleCode):
    def __init__(self, project: AppProject, config: NameConfig = NameConfig()):
        self.folder = ''
        self.filename = 'main'
        self.routes_folder = config.route_folder
        self.settings_filename = config.settings_file
        self.main_route_module = config.main_route_module()

    def __str__(self) -> str:
        return f"""from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .{self.main_route_module} import router
from .{self.settings_filename} import settings

app = FastAPI(title=settings.PROJECT_NAME)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_V1_STRING)
"""
