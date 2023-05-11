from fastapi import APIRouter
from pydantic import BaseModel


class Status(BaseModel):
    status: str


probe = APIRouter(tags=["probe"])


@probe.get('/liveness/', response_model=Status)
def liveness_probe() -> Status:
    return Status(status="OK")
