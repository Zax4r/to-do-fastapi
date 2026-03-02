from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.models.dependecies import DbDep
from app.core.jwt import create_access_token
from app.core.config import get_jwt_info
from app.core.security import authenticate_user, hash_password
from app.schemas.registrations import SRegister, SLogin
from app.services.users import UserService


router = APIRouter(prefix='/registration',tags=['Управление регистрацией'])

@router.post('/register/')
async def add_user(user: SRegister, session: DbDep):
    new_user_dict = user.model_dump()
    new_user_dict['password'] = hash_password(new_user_dict['password'])
    check = await UserService.add_one(session,**new_user_dict)
    if check:
        return {'message':f'Пользователь добавлен:{user}'}
    return {'message':f'Ошибка добавления пользователя:{user}'}

@router.post('/login/')
async def login(session: DbDep, response: Response, form: SLogin = Depends()):
    user = await authenticate_user(session, form.email, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    jwt_settings = get_jwt_info()
    token = create_access_token(
        {'sub':str(user.id)},expires_delta=jwt_settings['ACCESS_TOKEN_EXPIRE_MINUTES']
    )

    response.set_cookie('user_access_token',token, httponly=True)
    return { 'message': 'Авторизация успешна!'}

@router.post('/logout/')
async def login(response: Response):
    response.delete_cookie('user_access_token')
    return {'message':'Успешно вышел с аккаунта'}