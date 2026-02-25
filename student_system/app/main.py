from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import os
from app.students.router import students_router
from app.majors.router import majors_router
from app.users.router import users_router
from app.pages.router import pages_router
from fastapi.staticfiles import StaticFiles
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount('/static',StaticFiles(directory='app/static'),'static')

app.include_router(students_router)
app.include_router(majors_router)
app.include_router(users_router)
app.include_router(pages_router)

@app.get('/')
async def root():
    return RedirectResponse('/pages/students')

@app.middleware('http')
async def add_time_logging(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(process_time)
    return response
