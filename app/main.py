from api.probes import probe
from api.v1 import v1
from core.config import ApiSettings
from core.logging_middleware import LoggingMiddleware
from fastapi import FastAPI


def create_app() -> FastAPI:
    settings = ApiSettings(_env_file=".env")
    app = FastAPI(**settings.dict())
    app.include_router(probe, prefix=settings.probes_path)
    app.include_router(v1, prefix=settings.v1_path)
    app.add_middleware(LoggingMiddleware)
    return app


app = create_app()
