from app.service.base import BaseService
from app.majors.models import Major


class MajorsService(BaseService):
    model = Major