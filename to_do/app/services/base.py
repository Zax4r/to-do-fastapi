from sqlalchemy import select as sqlalchemy_select, insert as sqlalchemy_insert, delete as sqlalchemy_delete
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
    
    @classmethod
    async def add_one(cls, session: AsyncSession, **data):
        async with session.begin():
            new_entity = cls.model(**data)
            session.add(new_entity)
            return new_entity
        
    @classmethod
    async def delete_one_by_id(cls, session: AsyncSession, id):
        async with session.begin():
            result = await session.execute(
                sqlalchemy_select(cls.model)
                .where(cls.model.id == id)
                )
            entity = result.scalar_one_or_none()

            if not entity:
                return None
            
            await session.delete(entity)
            return id