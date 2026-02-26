from fastapi import Depends
from typing import Annotated
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

DbDep = Annotated[AsyncSession,Depends(get_db)]