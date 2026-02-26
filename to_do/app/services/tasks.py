from app.services.base import BaseService
from app.models.tasks import Task


class TaskService(BaseService):
    model=Task
