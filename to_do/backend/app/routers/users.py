from app.schemas.users import SUserAdd, SUserAnswer
from fastapi import APIRouter, HTTPException, status
from app.models.dependecies import DbDep
from typing import List
from app.services.users import UserService
from app.core.security import hash_password

router = APIRouter(prefix="/users", tags=["Работа с пользователем"])


@router.post("/add/", response_model=SUserAnswer)
async def add_user(user: SUserAdd, session: DbDep):
    new_user_dict = user.model_dump()
    new_user_dict["password"] = hash_password(new_user_dict["password"])
    check = await UserService.add_one(session, **new_user_dict)
    print(check)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error while adding user"
        )
    print(check)
    return check


@router.get("/", response_model=List[SUserAnswer])
async def get_users(session: DbDep):
    users = await UserService.get_all(session)
    return users


@router.get("/{user_id}", response_model=SUserAnswer)
async def get_user(user_id: int, session: DbDep):
    user = await UserService.get_one_or_none_by_field(session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No user with {user_id} found",
        )
    return user


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, session: DbDep):
    check = await UserService.delete_one_by_id(session, user_id)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No user with {user_id} found",
        )
    return {"message": f"User {user_id} deleted"}
