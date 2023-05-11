from typing import Optional

from pydantic import BaseSettings


class ApiSettings(BaseSettings):
    title: str = "Translate API"
    version: str = "0.1"
    root_path: str = ""
    openapi_usage: bool = True
    probes_path: str = "/probe"
    v1_path: str = "/v1"
    openapi_url: Optional[str] = "/openapi.json"
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
