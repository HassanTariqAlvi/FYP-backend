from datetime import datetime, timedelta

from app.models import DailyWork
from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService


class DailyWorkService:
    def get_dailywork_list(self):
        return DailyWork.objects.all()

    def get_dailywork_report(self, data):
        employee_service = EmployeeService()
        dailywork_service = DailyWorkService()

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
            employee = employee_service.get_contract_base_employee(
                pk=data['employee'])

            dailyWork = BaseService.serialize_object(
                'DailyWorkReadSerializer',
                employee.dailywork_set.filter(
                    date__gte=data['from_date'],
                    date__lte=data['to_date']
                ),
                many=True,
                module_name='DailyWorkSerializer'
            )
        else:
            dailyWork = BaseService.serialize_object(
                'DailyWorkReadSerializer',
                dailywork_service.get_dailywork_list().filter(
                    date__gte=data['from_date'],
                    date__lte=data['to_date']
                ),
                many=True,
                module_name='DailyWorkSerializer'
            )
        return {
            'data': dailyWork,
            'columns': [
                {
                    'field': "employee_name", 'headerName': "Name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "date", 'headerName': "Date", 'type': "date", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "unit_name", 'headerName': "Unit name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "total_pieces", 'headerName': "Total units", 'type': "number", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "price_per_unit",
                    'headerName': "Price/Unit",
                    'type': "number",
                    'flex': 1,
                    'minWidth': 150,
                },
                {
                    'field': "total_amount", 'headerName': "Total amount", 'type': "number", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "user", 'headerName': "Created by", 'flex': 1, 'minWidth': 150
                },
            ]
        }
