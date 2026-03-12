from app.services.base import BaseService
from app.models.tasks import Task
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, event, update


class TaskService(BaseService):
    model=Task


    @classmethod
    async def delete_task(cls, session: AsyncSession, task_id: int, user_id: int):
        result = await session.execute(select(cls.model)
                                    .where(cls.model.id==task_id))
        task = result.scalar_one_or_none()
        if not task:
            return None
        
        if task.user_id != user_id:
            return None
        try:
            await session.delete(task)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            return None

    @event.listens_for(Task,'after_delete')
    def update_after_deletion(mapper,connection,target):
        user_id = target.user_id
        if target.is_checked:
            connection.execute(
                update(User)
                .where(User.id==user_id)
                .values(completed_tasks = User.completed_tasks-1)
            )
        else:
            connection.execute(
                update(User)
                .where(User.id==user_id)
                .values(active_tasks = User.active_tasks-1)
            )

    @event.listens_for(Task,'after_insert')
    def update_after_insert(mapper,connection,target):
        user_id = target.user_id
        connection.execute(
            update(User)
            .where(User.id==user_id)
            .values(active_tasks = User.active_tasks+1))

    @classmethod
    async def update_one(cls, session: AsyncSession, id, **new_values):

        stmt = select(cls.model).where(cls.model.id == id)
        result = await session.execute(stmt)
        instance = result.scalar_one()
        if not instance:
            return False

        is_checked_changed = False
        if 'is_checked' in new_values:
            if instance.is_checked != new_values['is_checked']:
                is_checked_changed = True
                new_is_checked = new_values['is_checked']

        stmt = update(cls.model).where(cls.model.id == id).values(**new_values)
        await session.execute(stmt)

        if is_checked_changed:
            if new_is_checked:
                user_stmt = (
                    update(User)
                    .where(User.id == instance.user_id)
                    .values(
                        active_tasks=User.active_tasks - 1,
                        completed_tasks=User.completed_tasks + 1
                    )
                )
            else:
                user_stmt = (
                    update(User)
                    .where(User.id == instance.user_id)
                    .values(
                        active_tasks=User.active_tasks + 1,
                        completed_tasks=User.completed_tasks - 1
                    )
                )
            await session.execute(user_stmt)

        await session.commit()
        return True 