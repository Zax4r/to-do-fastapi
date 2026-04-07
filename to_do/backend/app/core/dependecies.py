from fastapi import Depends
from typing import Annotated
from app.core.jwt import get_current_user
from app.models.users import User

CUDep = Annotated[User, Depends(get_current_user)]
