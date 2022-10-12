from api.serializers.LoanDetailSerializer import LoanDetailSerializer, LoanDetailReportSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import LoanDetail
from app.services.BaseService import BaseService
from app.services.LoanDetailService import LoanDetailService
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class LoanDetailView(AbstractBaseView):
    model = LoanDetail
    queryset = LoanDetail.objects.all()
    serializer_class = LoanDetailSerializer
    loan_detail_service = LoanDetailService()
    post_message = 'Loan approved successfully!'

    @action(detail=True, methods=['post', 'put'])
    def approve_loan(self, request, *args, **kwargs):
        response = None
        loan_application = BaseService.get_instance(
            'Loan', pk=request.data['id'])

        loan_detail_exists = self.loan_detail_service.loan_detail_exists(
            employee=loan_application.employee)
        with transaction.atomic():
            loan_application.status = 'Approved'
            loan_application.save()
            if loan_detail_exists:
                instance = loan_application.employee.loandetail
                instance.user = self.request.user
                instance.total_loan_left += loan_application.loan_amount
                instance.loan_pending = True if instance.total_loan_left > 0 else False
                instance.save()
                response = Response({'message': self.post_message})
            else:
                request.data.clear()
                request.data['employee'] = loan_application.employee.id
                request.data['total_loan_left'] = loan_application.loan_amount
                request.data['loan_pending'] = True if loan_application.loan_amount > 0 else False
                response = self.create(request, *args, **kwargs)
        return response

    @action(detail=True, methods=['put'])
    def reject_loan(self, request, *args, **kwargs):
        loan_application = BaseService.get_instance(
            'Loan', pk=request.data['id'])
        loan_application.status = 'Rejected'
        loan_application.save()
        return Response({'message': 'Application for loan approval rejected successfully!'})

    @action(detail=False, methods=['post'])
    def generate_report(self, request, *args, **kwargs):
        loandetail_service = LoanDetailService()
        serializer = LoanDetailReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = loandetail_service.get_loandetail_report(
            serializer.validated_data
        )
        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            'columns': data['columns'],
        })
