from fastapi import APIRouter

from delvify.api.v1 import index, tasklists, tasks

ms_router = APIRouter(prefix="/api/v1", tags=["v1"])

ms_router.include_router(index.endpoint, prefix="/index", tags=["index"])
ms_router.include_router(tasklists.endpoint, prefix="/lists", tags=["lists"])
ms_router.include_router(tasks.endpoint, prefix="/tasks", tags=["tasks"])
