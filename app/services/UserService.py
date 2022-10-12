from app.services.BaseService import BaseService
from app.exceptions import AlreadyExists, DoesNotExist
from app.models import User

from .EmployeeService import EmployeeService
from .PermissionService import PermissionService


class UserService:
    employee_service = EmployeeService()
    permission_service = PermissionService()

    def get_account(self, **kwargs):
        return User.objects.get(**kwargs)

    def account_exists(self, employee):
        exists = User.objects.filter(employee=employee).exists()
        if not exists:
            raise DoesNotExist(
                detail='This employee does not have any account')

    def account_not_exists(self, employee):
        exists = User.objects.filter(employee=employee).exists()
        if exists:
            raise AlreadyExists(
                detail='This employee is already assigned an account')

    def get_add_user_data(self, **kwargs):
        employee_instance = self.employee_service.get_employee(**kwargs)
        self.account_not_exists(employee_instance)
        permissions = self.permission_service.get_permissions_list()
        employee_dict = self.employee_service.employee_dict(employee_instance)
        return {'employee_data': employee_dict, 'permissions_list': permissions}

    def get_edit_user_data(self, **kwargs):
        employee_instance = self.employee_service.get_employee(**kwargs)
        self.account_exists(employee_instance)
        account_instance = self.get_account(employee=employee_instance)
        allowed_permissions = self.permission_service.get_permissions_list(
            account_instance.user_permissions.all())
        other_permissions = self.permission_service.exclude_allowed_permissions(
            allowed_permissions, list_format=True)
        account_instance = BaseService.serialize_object(
            'UserSerializer', account_instance)
        employee_dict = self.employee_service.employee_dict(employee_instance)
        return {
            'employee_data': employee_dict,
            'account_data': account_instance,
            'allowed_permissions': allowed_permissions,
            'other_permissions': other_permissions
        }
