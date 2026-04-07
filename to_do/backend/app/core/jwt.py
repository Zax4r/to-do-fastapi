import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import get_jwt_info
from fastapi import Request, status, HTTPException, Depends
from app.services.users import UserService
from app.models.dependecies import DbDep


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )
    return token


def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(expires_delta)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    jwt_settings = get_jwt_info()
    encoded_jwt = jwt.encode(
        to_encode, jwt_settings["SECRET_KEY"], algorithm=jwt_settings["ALGORITHM"]
    )
    return encoded_jwt


async def get_current_user(session: DbDep, token: str = Depends(get_token)):
    try:
        jwt_settings = get_jwt_info()
        payload = jwt.decode(
            token, jwt_settings["SECRET_KEY"], algorithms=[jwt_settings["ALGORITHM"]]
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token does not contain data",
        )

    user = await UserService.get_one_or_none_by_field(session, id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token contains wrong data"
        )

    return user
