from api.serializers.OverTimeSerializer import OverTimeSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import OverTime
from app.services.AttendanceService import AttendanceService
from app.services.EmployeeService import EmployeeService
from app.services.OverTimeService import OverTimeService
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from app.exceptions import DoesNotExist


def timestamp_to_time(request):
    keys = request.data.keys()
    if 'start' in keys:
        request.data['start'] = datetime.fromtimestamp(
            request.data['start']/1000
        ).time().replace(microsecond=0)
    if 'end' in keys:
        request.data['end'] = datetime.fromtimestamp(
            request.data['end']/1000
        ).time().replace(microsecond=0)


class OverTimeView(AbstractBaseView):
    model = OverTime
    queryset = OverTime.objects.all()
    serializer_class = OverTimeSerializer
    post_message = "Over time record added successfully!"
    put_message = "Over time recored updated successfully!"
    delete_message = "Over time recored deleted successfully!"

    employee_service = EmployeeService()
    attendance_service = AttendanceService()

    def create(self, request, *args, **kwargs):
        if request.data is None:
            raise DoesNotExist(detail='Please fill the form')
        timestamp_to_time(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        timestamp_to_time(request)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        overtime_service = OverTimeService()
        overtime_service.save_overtime(
            self.request.user, serializer.validated_data)

    def perform_update(self, serializer):
        overtime_service = OverTimeService()
        overtime_service.update_overtime(
            serializer.data['id'],
            self.request.user,
            serializer.validated_data
        )

    @action(detail=True)
    def get_employee_details(self, request, *args, **kwargs):
        employee = self.employee_service.get_hour_base_employee(**kwargs)
        employee_details = self.employee_service.employee_dict(employee)
        return Response({'employee_details': employee_details})

    @action(detail=True, methods=['post'])
    def manual_attendance(self, request, *args, **kwargs):
        self.attendance_service.mark_manual_attendance(request, **kwargs)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': self.post_message})
