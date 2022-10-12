from django.db import transaction
from datetime import datetime, timedelta
from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService
from app.models import LoanRecovery


class LoanRecoveryService:
    def get_loanrecovery_list(self):
        return LoanRecovery.objects.all()

    def save_loan_recovery(self, user, loanDetail, recovery_date, deducted_amount):
        with transaction.atomic():
            loan_recovery = loanDetail.loanrecovery_set.create(
                user=user,
                deducted_amount=deducted_amount,
                recovery_date=recovery_date
            )
            # loanDetail.total_loan_left -= deducted_amount
            # loanDetail.loan_pending = True if loanDetail.total_loan_left > 0 else False
            # loanDetail.save()
            return loan_recovery

    def get_loanrecovery_report(self, data):
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
            loanrecovery = BaseService.serialize_object(
                'LoanRecoveryReportTableSerializer',
                self.get_loanrecovery_list().filter(
                    loanDetail=employee.id,
                    recovery_date__gte=data['from_date'],
                    recovery_date__lte=data['to_date']
                ),
                many=True,
                module_name='LoanRecoverySerializer'
            )
        else:
            loanrecovery = BaseService.serialize_object(
                'LoanRecoveryReportTableSerializer',
                self.get_loanrecovery_list().filter(
                    recovery_date__gte=data['from_date'],
                    recovery_date__lte=data['to_date']
                ),
                many=True,
                module_name='LoanRecoverySerializer'
            )
        return {
            'data': loanrecovery,
            'columns': [
                {
                    'field': "name", 'headerName': "Name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "department", 'headerName': "Department", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "phone_no", 'headerName': "Phone no", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "recovery_date", 'headerName': "Date", 'type': "date", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "deducted_amount", 'headerName': "Deducted amount", 'type': 'number', 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "user", 'headerName': "By", 'flex': 1, 'minWidth': 150
                },
            ]
        }
