from app.models import LoanDetail
from app.services.EmployeeService import EmployeeService
from app.services.BaseService import BaseService


class LoanDetailService:

    def get_loandetail_list(self):
        return LoanDetail.objects.all()

    def loan_detail_exists(self, **kwargs):
        return LoanDetail.objects.filter(**kwargs).exists()

    def get_loandetail_report(self, data):
        if data['employee_selection'] == 'One employee':
            loandetail = BaseService.serialize_object(
                'LoanDetailReportTableSerializer',
                self.get_loandetail_list().filter(
                    employee=data['employee']
                ),
                many=True,
                module_name='LoanDetailSerializer'
            )
        else:
            loandetail = BaseService.serialize_object(
                'LoanDetailReportTableSerializer',
                self.get_loandetail_list(),
                many=True,
                module_name='LoanDetailSerializer'
            )
        return {
            'data': loandetail,
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
                    'field': "total_loan_left", 'headerName': "Pending loan", 'type': 'number', 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "loan_pending", 'headerName': "Status", 'flex': 1, 'type': 'string', 'minWidth': 150
                },
                # {
                #     'field': "user", 'headerName': "By", 'flex': 1, 'minWidth': 150
                # },
            ]
        }
