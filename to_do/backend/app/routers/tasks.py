from fastapi import APIRouter, HTTPException, status
from app.services.tasks import TaskService
from app.schemas.tasks import STaskAdd, STaskShow, STaskUpd
from app.models.dependecies import DbDep
from app.core.dependecies import CUDep
from typing import List
from app.cache import set_cached,get_cached


router = APIRouter(prefix='/tasks',tags=['Работа с задачами'])

@router.post('/add/', response_model= STaskAdd)
async def add_task(add_task: STaskAdd, session: DbDep, user: CUDep):
    key = f'tasks:user:{user.id}'
    new_task = add_task.model_dump()
    new_task['user_id'] = user.id
    check = await TaskService.add_one(session,**new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with adding task"
        )
    cached_tasks = await get_cached(key)
    if cached_tasks is None:
        cached_tasks = []
    cached_tasks.append(STaskShow.model_validate(check).model_dump())
    await set_cached(key,cached_tasks)
    return check

@router.put('/update/{task_id}', response_model= STaskUpd)
async def update_task(task_id: int, task_upd: STaskUpd, session: DbDep, user: CUDep):
    key = f'tasks:user:{user.id}'
    new_task = task_upd.model_dump()
    check = await TaskService.update_one(session, task_id, **new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with updating task"
        )
    cached_tasks = await get_cached(key)
    for i in range(len(cached_tasks)):
        if cached_tasks[i]['id']==task_id:
            cached_tasks[i] = STaskShow.model_validate(check).model_dump()
            break
    await set_cached(key, cached_tasks)
    return task_upd



@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: DbDep, user: CUDep):
    key = f'tasks:user:{user.id}'
    check = await TaskService.delete_task(session, task_id, user.id)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with deleting task"
        )
    cached_tasks = await get_cached(key)
    for i in range(len(cached_tasks)):
        if cached_tasks[i]['id']==task_id:
            cached_tasks.pop(i)
            break
    await set_cached(key, cached_tasks)
    return {'message': f'Task deleted'}


@router.get('/', response_model=List[STaskShow])
async def get_all(session: DbDep, user: CUDep):
    key = f'tasks:user:{user.id}'
    tasks_cached = await get_cached(key)
    if tasks_cached:
        return tasks_cached
    tasks = await TaskService.get_all(session, user_id = user.id)
    tasks_dicts = [STaskShow.model_validate(t).model_dump() for t in tasks] 
    await set_cached(key, tasks_dicts)
    return tasks_dicts
