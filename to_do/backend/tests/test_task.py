import pytest

@pytest.mark.asyncio
async def test_get_tasks(async_client):
    res = await async_client.get('/tasks/')
    json = res.json()
    assert res.status_code == 401
    assert json['detail'] == 'Token not found'

@pytest.mark.asyncio
async def test_user_tasks_add(async_client, user_authenticated):
    res = await async_client.get('/tasks/')
    json = res.json()
    assert res.status_code == 200
    assert json == []

    res = await async_client.post('/tasks/add/',
                                  json={'task_name':'test_task',
                                         'task_description': 'test_task_descr'})
    
    assert res.status_code == 200
    json = res.json()
    assert json['task_name'] == 'test_task'
    assert json['task_description'] == 'test_task_descr'

    res = await async_client.get('/tasks/')
    json = res.json()
    assert res.status_code == 200
    assert len(json) == 1

    res = await async_client.get('/users/1')
    json = res.json()
    assert res.status_code == 200
    assert json['active_tasks'] == 1


@pytest.mark.asyncio
async def test_user_tasks_update(async_client, user_authenticated):

    res = await async_client.post('/tasks/add/',
                                  json={'task_name':'test_task_old',
                                         'task_description': 'test_task_descr'})

    res = await async_client.get('/tasks/')
    json = res.json()
    assert res.status_code == 200
    assert json[0]['task_name'] == 'test_task_old'

    res = await async_client.put('/tasks/update/1',
                                 json={'task_name':'test_task_new',
                                       'task_description': 'test_task_descr',
                                       'is_checked': True})
    assert res.status_code == 200

    res = await async_client.get('/tasks/')
    json = res.json()
    assert json[0]['task_name'] == 'test_task_new'

    res = await async_client.get('/users/1')
    json = res.json()
    assert json['active_tasks'] == 0
    assert json['completed_tasks'] == 1


@pytest.mark.asyncio
async def test_user_tasks_delete(async_client, user_authenticated):

    res = await async_client.post('/tasks/add/',
                                  json={'task_name':'test_task_old',
                                         'task_description': 'test_task_descr'})

    res = await async_client.get('/tasks/')
    json = res.json()
    assert res.status_code == 200
    assert json[0]['task_name'] == 'test_task_old'

    res = await async_client.delete('/tasks/delete/1')
    assert res.status_code == 200

    res = await async_client.get('/tasks/')
    json = res.json()
    assert len(json) == 0

    res = await async_client.get('/users/1')
    json = res.json()
    assert json['active_tasks'] == 0
    assert json['completed_tasks'] == 0