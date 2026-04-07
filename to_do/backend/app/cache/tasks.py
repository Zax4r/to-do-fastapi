from app.cache.base import BaseCacheService


class TaskCacheService(BaseCacheService):
    def __init__(self, redis_client):
        super().__init__(redis_client)
        self.base_prefix = "tasks"
