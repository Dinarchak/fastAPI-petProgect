from app.service.base import BaseService
from app.users.models import User
from app.users.models import Role

class UsersService(BaseService):
    model = User


class RolesService(BaseService):
    model = Role