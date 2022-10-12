from app.exceptions import DoesNotExist, InvalidNumber
from app.models import Employee


class EmployeeService:

    def get_all_employees(self):
        return Employee.objects.all()

    def __employee_exists(self, **kwargs):
        exists = Employee.objects.filter(**kwargs).exists()
        if not exists:
            raise DoesNotExist(detail='This employee does not exist')
        return exists

    def __get_employee(self, **kwargs):
        kwargs = self.int_to_str(**kwargs)
        if not kwargs['pk'].isdigit():
            raise InvalidNumber(detail='Please enter valid employee id')

        if self.__employee_exists(**kwargs):
            return Employee.objects.get(**kwargs)

    def get_employee(self, **kwargs):
        employee = self.__get_employee(**kwargs)
        return employee

    def get_contract_base_employee(self, **kwargs):
        employee = self.__get_employee(**kwargs)
        if not employee.employee_type.name == 'Contract':
            raise DoesNotExist(
                detail='This employee is not hired on contract basis')
        return employee

    def get_hour_base_employee(self, **kwargs):
        employee = self.__get_employee(**kwargs)
        if employee.employee_type.name == 'Contract':
            raise DoesNotExist(
                detail='This employee is hired on contract basis')
        return employee

    def get_loanee_employee(self, **kwargs):
        employee = self.__get_employee(**kwargs)
        try:
            loanDetail = employee.loandetail
            return employee
        except:
            raise DoesNotExist(
                detail='This employee does not have pending loan')

    def employee_dict(self, instance):
        return{
            "image": f"http://localhost:8000{instance.image.url}",
            "Name": instance.name,
            "Department": instance.department.name,
            "CNIC": instance.cnic,
            "Phone no": instance.phone_no
        }

    def int_to_str(self, **kwargs):
        if isinstance(kwargs['pk'], int):
            kwargs['pk'] = str(kwargs['pk'])
        return kwargs
