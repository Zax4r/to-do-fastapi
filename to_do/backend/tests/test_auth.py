import pytest

@pytest.mark.asyncio
async def test_auth_user(async_client, user_created):
    res = await async_client.post('/registration/login/',
                                  json={'email':'testuser@email.com',
                                         'password': 'password'})
    
    json = res.json()
    assert json['message'] == 'Авторизация успешна!'