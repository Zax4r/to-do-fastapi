from sqlalchemy import select as sqlalchemy_select, insert as sqlalchemy_insert
from sqlalchemy.ext.asyncio import AsyncSession

class BaseService:
    model = None

    @classmethod
    async def get_all(cls,session: AsyncSession, **filters):
        query = sqlalchemy_select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        res = result.scalars()
        return res

    @classmethod
    async def get_one_or_none_by_id(cls, session: AsyncSession, id):
        query = sqlalchemy_select(cls.model).where(cls.model.id == id)
        result = await session.execute(query)
        res = result.scalar_one_or_none()
        return res