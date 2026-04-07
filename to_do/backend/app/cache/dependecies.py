from fastapi import Depends, Request
from typing import Annotated
from app.cache.tasks import TaskCacheService


async def get_task_cache_dep(request: Request):
    return TaskCacheService(request.app.state.redis_client)


TCDep = Annotated[TaskCacheService, Depends(get_task_cache_dep)]
