from fastapi import APIRouter

from delvify.api.v1 import index

ms_router = APIRouter(prefix="/api/v1", tags=["v1"])

ms_router.include_router(index.endpoint, prefix="/index", tags=["index"])
