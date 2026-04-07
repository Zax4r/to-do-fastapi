from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TimeLogger")


class TimeLoggerMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        end = time.perf_counter()
        self.logger.info(f"Call |{request.method}:{request.url.path}| took {end-start}")
        return response
