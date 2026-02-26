from app.schemas.users import SUserAdd, SUserAnswer
from fastapi import APIRouter
from app.dependecies import DbDep
from typing import List
from app.services.users import UserService


router = APIRouter(prefix='/users',tags=['Работа с пользователем'])

@router.post('/add/')
async def add_user(user: SUserAdd):
    return user

@router.get('/', response_model=List[SUserAnswer])
async def get_users(session: DbDep):
    users = await UserService.get_all(session)
    return users

@router.get('/{user_id}', response_model=SUserAnswer)
async def get_user(user_id:int, session: DbDep):
    user = await UserService.get_one_or_none_by_id(session,user_id)
    return user