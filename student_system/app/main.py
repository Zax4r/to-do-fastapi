from fastapi import FastAPI
import os
from app.students.router import router_students
from app.majors.router import router_majors




app = FastAPI()

app.include_router(router_students)
app.include_router(router_majors)

