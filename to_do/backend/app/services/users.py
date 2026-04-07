from app.models.users import User
from app.services.base import BaseService


class UserService(BaseService):
    model = User
