from api.serializers.DailyWorkSerializer import (DailyWorkReadSerializer,
                                                 DailyWorkSerializer, DailyWorkReportSerializer)
from api.views.AbstractBaseView import AbstractBaseView
from app.models import DailyWork
from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService
from app.services.DailyWorkService import DailyWorkService
from app.services.UnitPriceService import UnitPriceService
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class DailyWorkView(AbstractBaseView):
    employee_service = EmployeeService()
    unit_price_service = UnitPriceService()

    model = DailyWork
    queryset = DailyWork.objects.all()
    post_message = 'Daily work report saved successfully!'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return DailyWorkSerializer
        return DailyWorkReadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if data is not None:
            keys = request.data.keys()
            fields = ['department', 'unit', 'criteria']

            if 'employee' in keys:
                request.data['employee'] = BaseService.get_instance(
                    'Employee', id=data['employee']).id

            if(all(field in keys for field in fields)):
                request.data['unit_price'] = BaseService.get_instance(
                    'UnitPrice',
                    department=BaseService.get_instance(
                        'Department', name=data['department']).id,
                    unit=BaseService.get_instance(
                        'Unit', name=data['unit']).id,
                    criteria=BaseService.get_instance(
                        'MeasureCriteria', name=data['criteria']).id,
                ).id
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        for key in ['unit', 'department', 'criteria']:
            del serializer.validated_data[key]
        DailyWork.objects.create(user, **serializer.validated_data)

    @action(detail=True)
    def add_daily_work(self, request, *args, **kwargs):
        employee_data = self.employee_service.get_contract_base_employee(
            **kwargs)
        unit_prices = self.unit_price_service.filter_unit_prices(
            queryset=None, department=employee_data.department)
        unit_prices = BaseService.serialize_object(
            'UnitPriceSerializer', unit_prices, many=True)
        return Response({'employee_data': {
            "image": f"http://localhost:8000{employee_data.image.url}",
            "Name": employee_data.name,
            "Department": employee_data.department.name,
            "CNIC": employee_data.cnic,
            "Phone no": employee_data.phone_no,
        }, 'unit_prices': unit_prices})

    @action(detail=False, methods=['post'])
    def generate_report(self, request, *args, **kwargs):
        dailywork_service = DailyWorkService()
        serializer = DailyWorkReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dailywork_service.get_dailywork_report(
            serializer.validated_data
        )
        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            'columns': data['columns'],
        })
