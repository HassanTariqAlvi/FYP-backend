from datetime import datetime, timedelta

from app.models import Role, Salary, SalaryGeneration
from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService
from app.services.LoanDetailService import LoanDetailService
from app.services.LoanRecoveryService import LoanRecoveryService
from app.services.SalaryGenerationService import SalaryGenerationService
from app.services.SalarySlipService import SalarySlipService
from django.db import transaction

month_days = {
    '1': 31,
    '2': 29 if datetime.now().date().year % 4 == 0 else 28,
    '3': 31,
    '4': 30,
    '5': 31,
    '6': 30,
    '7': 31,
    '8': 31,
    '9': 30,
    '10': 31,
    '11': 30,
    '11': 31,
}

months = {
    'January': 1,
    'Feburary': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}


class SalaryService:
    def get_salaries_list(self, **kwargs):
        return Salary.objects.all()

    def get_salary_details(self, data):
        employee_service = EmployeeService()
        employee = employee_service.get_employee(
            pk=data['employee']
        )
        employee_dict = employee_service.employee_dict(employee)

        employee_type = employee.employee_type.name
        if employee_type == 'Contract':
            salary_details = self.contract_base_salary_calculation(
                employee, data['salary'])
        elif employee_type == 'Hourly':
            salary_details = self.hourly_based_salary_calculation(
                employee, data['salary'])
        salary_details['employee_dict'] = employee_dict
        return salary_details

    def calculate_contract_base_amount(self, queryset):
        total_amount = 0
        for record in queryset:
            total_amount += record.total_amount
        return total_amount

    def contract_base_salary_calculation(self, employee, salary):
        loan_detail_service = LoanDetailService()
        salary = employee.salary_set.get(pk=salary)

        total_loan_left = employee.loandetail.total_loan_left if loan_detail_service.loan_detail_exists(
            employee=employee) else 0
        return {
            "table_data": {
                "Previous loan": total_loan_left,
                "Loan deduction": 0,
                "Remaining loan": total_loan_left,
                "Total salary": salary.total_salary,
                "Net salary": salary.total_salary,
                "From": salary.from_date,
                "To": salary.to_date
            },
            "details": {
                "salary": salary.id,
                "employee": employee.id,
                "from_date": salary.from_date,
                "to_date": salary.to_date,
                "total_salary": salary.total_salary,
                "net_salary": salary.total_salary,
                "is_deducted": False,
                "deducted_amount": 0
            }
        }

    def calculate_hourly_base_amount(self, queryset, rate):
        total_hours = 0
        for record in queryset:
            total_hours += record.worked_hours
        return (total_hours * rate, total_hours)

    def hourly_based_salary_calculation(self, employee, salary):
        loan_detail_service = LoanDetailService()
        salary = employee.salary_set.get(pk=salary)
        overtime = employee.overtime_set.filter(
            date__gte=salary.from_date,
            date__lte=salary.to_date
        )

        overtime_amount, total_hours = self.calculate_hourly_base_amount(
            overtime,
            Role.objects.get(name="Per Hour rate").salary
            # employee.employee_type.rolesalary.salary
        )

        total_loan_left = employee.loandetail.total_loan_left if loan_detail_service.loan_detail_exists(
            employee=employee) else 0
        return {
            "table_data": {
                "From": salary.from_date,
                "To": salary.to_date,
                "Previous loan": total_loan_left,
                "Remaining loan": total_loan_left,
                "Total hours": total_hours,
                "Overtime amount": overtime_amount,
                "Loan deduction": 0,
                "Total salary": salary.total_salary,
                "Net salary": salary.total_salary,
            },
            "details": {
                "salary": salary.id,
                "employee": employee.id,
                "from_date": salary.from_date,
                "to_date": salary.to_date,
                "total_salary": salary.total_salary,
                "net_salary": salary.total_salary,
                "is_deducted": False,
                "deducted_amount": 0,
                "overtime_amount": overtime_amount
            }
        }

    def save_salary(self, user, data):
        employee_service = EmployeeService()
        salary_slip_service = SalarySlipService()
        loan_recovery_service = LoanRecoveryService()

        employee = employee_service.get_employee(pk=data['employee'])

        with transaction.atomic():
            salary = employee.salary_set.get(pk=data['salary'])
            salary.total_salary = data['total_salary']
            salary.net_salary = data['net_salary']
            salary.issue_date = datetime.now().date()
            salary.paid = True
            salary.paid_by = user
            salary.save()

            if data['is_deducted']:
                loanDetail = employee.loandetail
                loan_recovery = loan_recovery_service.save_loan_recovery(
                    user=user,
                    loanDetail=loanDetail,
                    recovery_date=datetime.now().date(),
                    deducted_amount=data['deducted_amount']
                )
            else:
                loan_recovery = None

            salary_slip_service.save_salary_slip(
                salary=salary,
                loanRecovery=loan_recovery,
                is_loan_deducted=data['is_deducted'],
                user=user
            )

    def generate_one_employee_salary(self, user, data):
        employee_service = EmployeeService()
        employee = employee_service.get_employee(pk=data['employee'])
        if employee.employee_type.name == 'Hourly':
            self.hourly_based_salary_calculation_Manual(user, employee, data)
        elif employee.employee_type.name == 'Contract':
            self.contract_base_salary_calculation_Manual(user, employee, data)

    def hourly_based_salary_calculation_Manual(self, user, employee_instance, data):
        salaries = employee_instance.salary_set.all()
        # # attendance = employee_instance.attendance_set.all()
        overtime = employee_instance.overtime_set.all()
        month_no = data['generate_date'].month - 1
        prev = data['generate_date'] - \
            timedelta(days=month_days[f'{month_no}'])
        from_date = datetime(
            day=1,
            month=prev.month,
            year=prev.year,
        ).date()
        to_date = datetime(
            day=month_days[f'{month_no}'],
            month=from_date.month,
            year=from_date.year
        ).date()

        overtime = overtime.filter(
            date__gte=from_date,
            date__lte=to_date
        )

        if overtime.count() != 0:
            total_amount, total_hours = self.calculate_hourly_base_amount(
                overtime,
                Role.objects.get(name="Per Hour rate").salary
            )
            total_amount += employee_instance.role.salary

            employee_instance.salary_set.create(
                from_date=from_date,
                to_date=to_date,
                total_salary=total_amount,
                net_salary=total_amount,
                paid=False,
                user=user
            )

    def contract_base_salary_calculation_Manual(self, user, employee_instance, data):
        salaries = employee_instance.salary_set.all()
        daily_work = employee_instance.dailywork_set.all()

        month_no = data['generate_date'].month - 1
        prev = data['generate_date'] - \
            timedelta(days=month_days[f'{month_no}'])
        from_date = datetime(
            day=1,
            month=prev.month,
            year=prev.year,
        ).date()
        to_date = datetime(
            day=month_days[f'{month_no}'],
            month=from_date.month,
            year=from_date.year
        ).date()

        daily_work = daily_work.filter(
            date__gte=from_date,
            date__lte=to_date
        )

        if daily_work.count() != 0:
            total_amount = self.calculate_contract_base_amount(daily_work)

            employee_instance.salary_set.create(
                from_date=from_date,
                to_date=to_date,
                total_salary=total_amount,
                net_salary=total_amount,
                paid=False,
                user=user
            )

    def generate_all_employees_salary(self, user, data):
        employee_service = EmployeeService()
        salary_generation_service = SalaryGenerationService()
        salary_generation_service.check_salary_generated_or_not(
            data['generate_date']
        )

        employees = employee_service.get_all_employees()
        with transaction.atomic():
            SalaryGeneration.objects.create(user, **data)
            for employee in employees:
                if employee.employee_type.name == 'Hourly':
                    self.hourly_based_salary_calculation_Manual(
                        user,
                        employee,
                        data
                    )
                elif employee.employee_type.name == 'Contract':
                    self.contract_base_salary_calculation_Manual(
                        user, employee, data
                    )

    def get_salary_report(self, data):
        salary_service = SalaryService()
        employee_service = EmployeeService()

        month_no = months[data['month']]
        from_date = datetime(int(data['year']), month_no, 1).date()
        to_date = datetime(int(data['year']),
                           month_no, month_days[f'{month_no}']).date()

        if data['employee_selection'] == 'One employee':
            employee = employee_service.get_employee(
                pk=data['employee'])

            data = BaseService.serialize_object(
                'SalaryReportTableSerializer',
                employee.salary_set.filter(
                    from_date__gte=from_date,
                    to_date__lte=to_date,
                    paid=True if data['status'] == 'Paid' else False
                ),
                many=True,
                module_name="SalarySerializer"
            )
        else:
            data = BaseService.serialize_object(
                'SalaryReportTableSerializer',
                self.get_salaries_list().filter(
                    from_date__gte=from_date,
                    to_date__lte=to_date,
                    paid=True if data['status'] == 'Paid' else False
                ),
                many=True,
                module_name="SalarySerializer"
            )

        return {
            'data': data,
            'columns': [
                {
                    'field': "employee_id", 'headerName': "Employee id", 'flex': 1, 'minWidth': 150, 'type': 'number'
                },
                {
                    'field': "name", 'headerName': "Name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "from_date", 'headerName': "From", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "to_date", 'headerName': "To", 'flex': 1, 'minWidth': 150,
                },
                {
                    'field': "is_loan_deducted", 'headerName': "Is loan deducted", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "deducted_amount", 'headerName': "Loan deduction", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "total_loan_left", 'headerName': "Remaining loan", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "total_salary", 'headerName': "Total salary", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "net_salary", 'headerName': "Net salary", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "paid_by", 'headerName': "By", 'flex': 1, 'minWidth': 150
                },
            ]
        }
