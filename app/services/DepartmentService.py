from app.exceptions import DoesNotExist, InvalidNumber
from app.models import Department


class DepartmentService:
    pass
    # def __department_exists(self, **kwargs):
    #     exists = Department.objects.filter(**kwargs).exists()
    #     if not exists:
    #         raise DoesNotExist(detail='This department does not exist')
    #     return exists

    # def __get_department(self, **kwargs):
    #     if not kwargs['pk'].isdigit():
    #         raise InvalidNumber(detail='Please enter valid department id')

    #     if self.__department_exists(**kwargs):
    #         return Department.objects.get(**kwargs)

    # def get_department(self, **kwargs):
    #     department = self.__get_department(**kwargs)
    #     return department
