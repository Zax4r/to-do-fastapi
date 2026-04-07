from pwdlib import PasswordHash
from app.services.users import UserService

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


async def authenticate_user(session, email: str, password: str):
    user = await UserService.get_one_or_none_by_field(session, email=email)
    if not user:
        return False
    check = verify_password(password, user.password)
    if not check:
        return False
    return user
