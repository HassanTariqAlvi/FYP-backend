from api.serializers.LoanSerializer import LoanSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.exceptions import DeletionFailed, UpdationFailed
from app.models import Loan
from app.services.EmployeeService import EmployeeService
from app.services.LoanDetailService import LoanDetailService
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response


class LoanView(AbstractBaseView):
    model = Loan
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    employee_service = EmployeeService()
    loan_detail_service = LoanDetailService()
    post_message = 'Application for loan approval submitted successfully!'
    put_message = 'Application for loan approval updated successfully!'
    delete_message = 'Application for loan approval deleted successfully!'

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'loan_amount']

    def update(self, request, *args, **kwargs):
        if request.data['status'] == 'Approved':
            raise UpdationFailed(
                detail="Loan of this employee is already approved. Cannot update the application data")
        if request.data['status'] == 'Rejected':
            raise UpdationFailed(
                detail="Loan of this employee is already rejected. Cannot update the application data")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        loan_application = Loan.objects.get(**kwargs)
        if loan_application.status == 'Approved':
            raise DeletionFailed(
                detail="Loan of this employee is already approved. Cannot delete the application data")
        return super().destroy(request, *args, **kwargs)

    @action(detail=True)
    def add_loan(self, request, *args, **kwargs):
        employee = self.employee_service.get_employee(**kwargs)
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
