from fastapi import APIRouter, HTTPException, status
from app.services.tasks import TaskService
from app.schemas.tasks import STaskAdd, STaskShow, STaskUpd
from app.models.dependecies import DbDep
from app.core.dependecies import CUDep
from typing import List
from app.cache.dependecies import TCDep


router = APIRouter(prefix='/tasks',tags=['Работа с задачами'])

@router.post('/add/', response_model= STaskAdd)
async def add_task(add_task: STaskAdd, session: DbDep, user: CUDep, cache: TCDep):
    user_id = user.id
    new_task = add_task.model_dump()
    new_task['user_id'] = user_id
    check = await TaskService.add_one(session,**new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with adding task"
        )
    cached_tasks = await cache.get(user_id)
    if cached_tasks is not None:
        cached_tasks.append(STaskShow.model_validate(check).model_dump())
        await cache.set(user_id,cached_tasks)
    return check

@router.put('/update/{task_id}', response_model= STaskUpd)
async def update_task(task_id: int, task_upd: STaskUpd, session: DbDep, user: CUDep, cache: TCDep):
    user_id = user.id
    new_task = task_upd.model_dump()
    check = await TaskService.update_one(session, task_id, **new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with updating task"
        )
    cached_tasks = await cache.get(user_id)
    if cached_tasks is not None:
        for i in range(len(cached_tasks)):
            if cached_tasks[i]['id']==task_id:
                cached_tasks[i] = STaskShow.model_validate(check).model_dump()
                break
        await cache.set(user_id, cached_tasks)
    return task_upd



@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: DbDep, user: CUDep, cache: TCDep):
    user_id = user.id
    check = await TaskService.delete_task(session, task_id, user_id)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with deleting task"
        )
    cached_tasks = await cache.get(user_id)
    if cached_tasks is not None:
        for i in range(len(cached_tasks)):
            if cached_tasks[i]['id']==task_id:
                cached_tasks.pop(i)
                break
        await cache.set(user_id, cached_tasks)
    return {'message': f'Task deleted'}


@router.get('/', response_model=List[STaskShow])
async def get_all(session: DbDep, user: CUDep, cache: TCDep):
    user_id = user.id
    tasks_cached = await cache.get(user_id)
    if tasks_cached:
        return tasks_cached
    tasks = await TaskService.get_all(session, user_id = user_id)
    tasks_dicts = [STaskShow.model_validate(t).model_dump() for t in tasks] 
    await cache.set(user_id, tasks_dicts)
    return tasks_dicts
