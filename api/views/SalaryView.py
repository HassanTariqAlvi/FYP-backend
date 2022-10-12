from api.serializers.SalarySerializer import (SalaryReadSerializer,
                                              SalarySerializer,
                                              GenerateSalarySerializer, SalaryReportSerializer)
from app.models import Salary
from app.services.EmployeeService import EmployeeService
from app.services.SalaryService import SalaryService
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from app.exceptions import DoesNotExist


class SalaryView(viewsets.ModelViewSet):
    queryset = Salary.objects.all()

    def get_serializer_class(self):
        if self.action in ['list']:
            return SalaryReadSerializer
        return SalarySerializer

    def update(self, request, *args, **kwargs):
        salary_service = SalaryService()
        if request.data is not None:
            if 'is_deducted' in request.data.keys():
                if request.data['is_deducted']:
                    request.data['net_salary'] = request.data['total_salary'] - \
                        int(request.data['deducted_amount'])
                elif request.data['is_deducted'] == False:
                    request.data['deducted_amount'] = 0
        validated_data = self.get_validated_data(request)
        salary_service.save_salary(self.request.user, validated_data)
        return Response({'status_code': status.HTTP_200_OK, 'message': 'Salary calculated successfully!'})

    def get_validated_data(self, request):
        serializer = SalarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    @action(detail=False, methods=['post'])
    def get_salary_details(self, request, *args, **kwargs):

        salary_service = SalaryService()
        salary_details = salary_service.get_salary_details(request.data)
        return Response({
            'employee_data': salary_details['employee_dict'],
            "salary_table": salary_details["table_data"],
            "salary_details": salary_details["details"]
        })

    @action(detail=False, methods=['post'])
    def generate_salary(self, request, *args, **kwargs):
        if request.data is None:
            raise DoesNotExist(detail="Please fill the form")
        salary_service = SalaryService()
        request.data['generate_time'] = datetime.now().time()

        serializer = GenerateSalarySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        salary_service.generate_all_employees_salary(
            request.user,
            serializer.validated_data
        )
        return Response({
            "status_code": status.HTTP_201_CREATED,
            'message': "Salaries generated successfully!"
        })

    @action(detail=False, methods=['post'])
    def generate_report(self, request, *args, **kwargs):
        salary_service = SalaryService()        
        serializer = SalaryReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = salary_service.get_salary_report(
            serializer.validated_data
        )
        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            'columns': data['columns'],
        })
