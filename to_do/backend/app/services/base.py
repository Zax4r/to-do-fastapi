from sqlalchemy import (
    select as sqlalchemy_select,
    insert as sqlalchemy_insert,
    delete as sqlalchemy_delete,
    update as sqlalchemy_update,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, **filters):
        query = sqlalchemy_select(cls.model).filter_by(**filters)
        result = await session.execute(query)
        res = result.scalars()
        return res

    @classmethod
    async def get_one_or_none_by_field(cls, session: AsyncSession, **fields):
        query = sqlalchemy_select(cls.model).filter_by(**fields)
        result = await session.execute(query)
        res = result.scalar_one_or_none()
        return res

    @classmethod
    async def add_one(cls, session: AsyncSession, **data):
        new_entity = cls.model(**data)
        try:
            session.add(new_entity)
            await session.commit()
            await session.refresh(new_entity)
            return new_entity
        except Exception as e:
            await session.rollback()
            return False

    @classmethod
    async def update_one(cls, session: AsyncSession, id, **new_values):
        stmt = (
            sqlalchemy_update(cls.model).where(cls.model.id == id).values(**new_values)
        )
        try:
            await session.execute(stmt)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            return False

    @classmethod
    async def delete_one_by_id(cls, session: AsyncSession, id):
        result = await session.execute(
            sqlalchemy_select(cls.model).where(cls.model.id == id)
        )
        entity = result.scalar_one_or_none()

        if not entity:
            return None

        try:
            await session.delete(entity)
            await session.commit()
            return id
        except Exception as e:
            await session.rollback()
            return False
