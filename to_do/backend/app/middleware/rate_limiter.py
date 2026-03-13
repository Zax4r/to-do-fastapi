import redis.asyncio as redis
from fastapi import  HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_url: str, max_requests: int = 5, window_seconds: int = 10):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.redis = redis.from_url(redis_url)

    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        key = f'rate_limit:{client_ip}'

        permission = True

        try:
            current_count = await self.redis.incr(key,1)

            if current_count == 1:
                await self.redis.expire(key, self.window_seconds)
            
            if current_count > self.max_requests:
                permission = False
                ttl = await self.redis.ttl(key)
            
        except Exception as e:
            raise ConnectionError()
        
        if not permission:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                'detail':f'Too many requests try after {ttl} seconds'
                }
            )

        response = await call_next(request)
        return response
        
