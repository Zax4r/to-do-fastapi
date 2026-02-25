from fastapi import FastAPI
import os
from app.students.router import router_students
from app.majors.router import router_majors




app = FastAPI()

@app.on_event("startup")
async def startup_event():
    db_url = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL from env: {db_url}")

app.include_router(router_students)
app.include_router(router_majors)

