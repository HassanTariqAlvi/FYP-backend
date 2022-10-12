from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService
from app.services.AttendanceService import AttendanceService
from app.services.SalaryService import SalaryService
from app.services.DailyWorkService import DailyWorkService
from datetime import datetime, timedelta


class ReportService:
    def get_attendance_report(self, employee, data):
        attendance = BaseService.serialize_object(
            'AttendanceSerializer',
            employee.attendance_set.filter(
                date__gte=data['from_date'],
                date__lte=data['to_date']
            ),
            many=True,
        )
        return {
            'data': attendance,
            'columns': [
                {
                    'field': "name", 'headerName': "Name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "emp_in", 'headerName': "In", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "emp_out", 'headerName': "Out", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "worked_hours", 'headerName': "Total hours", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "date", 'headerName': "Date", 'flex': 1, 'minWidth': 150
                },
            ]
        }

    def get_salary_report(self, data):
        salary_service = SalaryService()
        employee_service = EmployeeService()

        if data['report_days'] == 'Last 7 days':
            data['to_date'] = datetime.now().date()
            data['from_date'] = datetime.now().date() - timedelta(days=7)
        elif data['report_days'] == 'Last 15 days':
            data['to_date'] = datetime.now().date()
            data['from_date'] = datetime.now().date() - timedelta(days=15)
        elif data['report_days'] == 'Last month':
            data['to_date'] = datetime.now().date()
            data['from_date'] = datetime.now().date() - timedelta(days=30)
        elif data['report_days'] == 'Custom':
            data['from_date'] = data['from_date']
            data['to_date'] = data['to_date']

        if data['employee_selection'] == 'One employee':
            employee = employee_service.get_employee(
                pk=data['employee'])

            data = BaseService.serialize_object(
                'SalaryReadSerializer',
                employee.salary_set.filter(
                    created_at__gte=data['from_date'],
                    created_at__lte=data['to_date'],
                    paid=True if data['status'] == 'Paid' else False
                ),
                many=True,
                module_name="SalarySerializer"
            )
        else:
            data = BaseService.serialize_object(
                'SalaryReportSerializer',
                salary_service.get_salaries_list().filter(
                    created_at__gte=data['from_date'],
                    created_at__lte=data['to_date'],
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
                    'field': "net_salary", 'headerName': "Net salary", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "total_salary", 'headerName': "Total salary", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "paid_by", 'headerName': "By", 'flex': 1, 'minWidth': 150
                },
            ]
        }
