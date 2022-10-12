from api.serializers.AttendanceSerializer import AttendanceSerializer, AttendanceReportSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import Attendance
from app.services.AttendanceService import AttendanceService
from app.services.EmployeeService import EmployeeService
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from app.exceptions import DoesNotExist


class AttendanceView(AbstractBaseView):
    model = Attendance
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    post_message = "Attendance marked successfully!"

    employee_service = EmployeeService()
    attendance_service = AttendanceService()

    def create(self, request, *args, **kwargs):
        if request.data is None:
            raise DoesNotExist(detail="Please enter employee id")
        employee = self.employee_service.get_hour_base_employee(
            pk=self.request.data['employee'])
        self.attendance_service.mark_attendance(
            self.request.user, employee)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': self.post_message})

    @action(detail=True)
    def get_attendance_details(self, request, *args, **kwargs):
        employee = self.employee_service.get_hour_base_employee(**kwargs)
        employee_details = self.employee_service.employee_dict(employee)
        attendace_details = self.attendance_service.get_attendance_details(
            employee)
        return Response({'attendance_data': attendace_details, 'employee_details': employee_details})

    @action(detail=True, methods=['post'])
    def manual_attendance(self, request, *args, **kwargs):
        self.attendance_service.mark_manual_attendance(request, **kwargs)
        return Response({'status_code': status.HTTP_201_CREATED, 'message': self.post_message})

    @action(detail=False, methods=['post'])
    def generate_report(self, request, *args, **kwargs):
        attendance_service = AttendanceService()
        serializer = AttendanceReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = attendance_service.get_attendance_report(
            serializer.validated_data
        )
        return Response({
            'status_code': status.HTTP_200_OK,
            'data': data['data'],
            'columns': data['columns'],
        })
