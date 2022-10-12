import datetime

from api.serializers.EmployeeSerializer import EmployeeSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import Employee
from app.services.BaseService import BaseService
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser


class EmployeeView(AbstractBaseView):
    model = Employee
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    parser_classes = [FormParser, MultiPartParser]
    post_message = "Employee registered successfully!"
    put_message = "Employee information updated successfully!"
    delete_message = "Employee information deleted successfully!"

    def __check_keys(self, request):
        keys = request.data.keys()
        data = request.data
        if 'department' in keys:
            data['department'] = BaseService.get_instance(
                'Department', name=data['department']).id

        if 'employee_type' in keys:
            data['employee_type'] = BaseService.get_instance(
                'EmployeeType', name=data['employee_type']).id

        if 'role' in keys:
            employee_type = BaseService.get_instance(
                'EmployeeType', pk=data['employee_type'])

            if employee_type.name == 'Contract':
                del data['role']
            else:
                data['role'] = BaseService.get_instance(
                    'Role',
                    # employee_type=employee_type,
                    name=data['role']
                ).id

        if 'joining_date' in keys:
            year, month, day = data['joining_date'].split('-')
            data['joining_date'] = datetime.date(
                int(year),
                int(month),
                int(day)
            )
        return request

    def __change_image_name(self, request):
        keys = request.data.keys()
        if 'cnic' in keys and 'image' in keys:
            imageType = request.data['image'].content_type.split('/')[1]
            request.data['image'].name = f"{request.data['cnic']}.{imageType}"
        return request

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request = self.__check_keys(request)
        request = self.__change_image_name(request)
        request.data._mutable = False
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        request = self.__check_keys(request)
        request = self.__change_image_name(request)
        request.data._mutable = False
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        Employee.objects.create(user, **serializer.validated_data)

    def perform_update(self, serializer):
        if 'image' in self.request.data.keys():
            instance = self.get_object()
            instance.image.delete()
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        instance.image.delete()
        return super().perform_destroy(instance)
