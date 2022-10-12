from api.serializers.LoanRecoverySerializer import LoanRecoverySerializer, LoanRecoveryReportSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import LoanRecovery
from app.services.EmployeeService import EmployeeService
from app.services.LoanDetailService import LoanDetailService
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from app.services.LoanRecoveryService import LoanRecoveryService


class LoanRecoveryView(AbstractBaseView):
    model = LoanRecovery
    queryset = LoanRecovery.objects.all()
    serializer_class = LoanRecoverySerializer
    employee_service = EmployeeService()
    loan_detail_service = LoanDetailService()
    post_message = 'Loan installment saved successfully!'

    def create(self, request, *args, **kwargs):
        if request.data is not None:
            if 'employee' in request.data:
                request.data['loanDetail'] = request.data['employee']
                del request.data['employee']
        return super().create(request, *args, **kwargs)

    @action(detail=True)
    def add_loan_recovery(self, request, *args, **kwargs):
        employee = self.employee_service.get_loanee_employee(**kwargs)
        loan_detail_exists = self.loan_detail_service.loan_detail_exists(
            employee=employee)
        return Response({
            'employee_data': {
                "image": f"http://localhost:8000{employee.image.url}",
                "Name": employee.name,
                "Department": employee.department.name,
                "CNIC": employee.cnic,
                "Phone no": employee.phone_no,
            },
            'loan_detail': {
                'Previous loan': employee.loandetail.total_loan_left if loan_detail_exists else 0,
                'Eligible': 'Yes'
            }
        })

    @action(detail=False, methods=['post'])
    def generate_report(self, request, *args, **kwargs):
        loanrecovery_service = LoanRecoveryService()
        serializer = LoanRecoveryReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = loanrecovery_service.get_loanrecovery_report(
            serializer.validated_data
        )
        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            'columns': data['columns'],
        })
