from fastapi import FastAPI
import redis.asyncio as redis
from app.routers.users import router as user_router
from app.routers.tasks import router as task_router
from app.routers.auth import router as auth_router
from app.core.config import get_redis_url
from app.middleware.rate_limiter import RateLimiterMiddleware
from app.middleware.time_logger import TimeLoggerMiddleware

async def lifespan(app):
    app.state.redis_client = redis.from_url(get_redis_url())
    yield 
    await app.state.redis_client.close()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    RateLimiterMiddleware,
    redis_url=get_redis_url(),
    max_requests=5,
    window_seconds=10
)

app.add_middleware(
    TimeLoggerMiddleware
)

app.include_router(user_router)
app.include_router(task_router)
app.include_router(auth_router)


@app.get('/')
async def root():
    return {'message':'Hello World'}
