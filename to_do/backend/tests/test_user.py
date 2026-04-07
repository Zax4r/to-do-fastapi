import pytest


@pytest.mark.asyncio
async def test_list_users(async_client):
    res = await async_client.get("/users/")
    json = res.json()

    assert json == []


@pytest.mark.asyncio
async def test_add_user(async_client):
    res = await async_client.post(
        "/users/add/",
        json={
            "email": "testuser@email.com",
            "username": "test_user",
            "password": "password",
        },
    )
    json = res.json()

    assert json["email"] == "testuser@email.com"
    assert "password" not in json
    assert json["active_tasks"] == 0


@pytest.mark.asyncio
async def test_list_users_after_adding_user(async_client):
    await async_client.post(
        "/users/add/",
        json={
            "email": "testuser@email.com",
            "username": "test_user",
            "password": "password",
        },
    )
    res = await async_client.get("/users/")
    json = res.json()

    assert len(json) == 1
    assert json[0]["username"] == "test_user"
    assert json[0]["email"] == "testuser@email.com"
    assert "password" not in json[0]


@pytest.mark.asyncio
async def test_get_user_by_id(async_client):
    await async_client.post(
        "/users/add/",
        json={
            "email": "testuser@email.com",
            "username": "test_user",
            "password": "password",
        },
    )
    res = await async_client.get("/users/1")
    json = res.json()

    assert json["username"] == "test_user"
    assert json["email"] == "testuser@email.com"
    assert "password" not in json


@pytest.mark.asyncio
async def test_get_user_by_id_fail(async_client):
    res = await async_client.get("/users/1")
    json = res.json()

    assert "username" not in json
    assert "email" not in json
    assert json["detail"] == "No user with 1 found"
