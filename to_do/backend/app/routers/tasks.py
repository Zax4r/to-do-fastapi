from fastapi import APIRouter, HTTPException, status
from app.services.tasks import TaskService
from app.schemas.tasks import STaskAdd, STaskShow, STaskUpd
from app.models.dependecies import DbDep
from app.core.dependecies import CUDep
from typing import List
from app.cache import set_cached,get_cached


router = APIRouter(prefix='/tasks',tags=['Работа с задачами'])

@router.post('/add/', response_model= STaskAdd)
async def add_task(add_task: STaskAdd, session: DbDep, current_user: CUDep):
    new_task = add_task.model_dump()
    new_task['user_id'] = current_user.id
    check = await TaskService.add_one(session,**new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with adding task"
        )
    return check

@router.put('/update/{task_id}', response_model= STaskUpd)
async def update_task(task_id: int, task_upd: STaskUpd, session: DbDep):
    new_task = task_upd.model_dump()
    check = await TaskService.update_one(session, task_id, **new_task)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with updating task"
        )
    return task_upd



@router.delete('/delete/{task_id}')
async def delete_task(task_id: int, session: DbDep, current_user: CUDep):
    check = await TaskService.delete_task(session, task_id, current_user.id)
    if not check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error with deleting task"
        )
    return {'message': f'Task deleted'}


@router.get('/', response_model=List[STaskShow])
async def get_all(session: DbDep, user: CUDep):
    tasks_cached = await get_cached(f'tasks:user:{user.id}')
    if tasks_cached:
        return tasks_cached
    tasks = await TaskService.get_all(session, user_id = user.id)
    tasks_dicts = [STaskShow.model_validate(t).model_dump() for t in tasks] 
    await set_cached(f'tasks:user:{user.id}', tasks_dicts)
    return tasks_dicts
