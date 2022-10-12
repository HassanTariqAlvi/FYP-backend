import random
from datetime import datetime, timedelta

from app.exceptions import DoesNotExist, InvalidFormat
from app.models import Attendance
from app.services.BaseService import BaseService
from app.services.EmployeeService import EmployeeService


def timestamp_to_time(request):
    keys = request.data.keys()
    if 'emp_in' in keys:
        request.data['emp_in'] = datetime.fromtimestamp(
            request.data['emp_in']/1000
        ).time().replace(microsecond=0)
    if 'emp_out' in keys:
        request.data['emp_out'] = datetime.fromtimestamp(
            request.data['emp_out']/1000
        ).time().replace(microsecond=0)


class AttendanceService:
    def get_attendance_list(self):
        return Attendance.objects.all()

    def filter_attendance(self, employee):
        return employee.attendance_set.filter(date=datetime.now().date()).last()

    def mark_attendance(self, user, employee_instance):
        attendance = employee_instance.attendance_set.filter(
            date=datetime.now().date()).last()
        if attendance is None:
            employee_instance.attendance_set.create(
                employee=employee_instance,
                emp_in=datetime.now().time().replace(microsecond=0),
                date=datetime.now().date(),
                user=user
            )
        elif attendance.emp_out is None:
            attendance.emp_out = datetime.now().time().replace(microsecond=0)
            # attendance.worked_hours = attendance.emp_out.hour - attendance.emp_in.hour
            attendance.worked_hours = random.randint(1, 10)
            attendance.save()
        elif attendance.emp_in and attendance.emp_out:
            employee_instance.attendance_set.create(
                employee=employee_instance,
                emp_in=datetime.now().time().replace(microsecond=0),
                date=datetime.now().date(),
                user=user
            )

    def get_attendance_details(self, employee_instance):
        attendance = employee_instance.attendance_set.filter(
            date=datetime.now().date()).last()
        return {
            "image": f"http://localhost:8000{employee_instance.image.url}",
            "Name": employee_instance.name,
            "Department": employee_instance.department.name,
            "In": attendance.emp_in if attendance else "-",
            "Out": attendance.emp_out if attendance else "-"
        }

    def mark_manual_attendance(self, request, **kwargs):
        employee_service = EmployeeService()
        employee = employee_service.get_hour_base_employee(**kwargs)
        attendance = self.filter_attendance(employee)
        timestamp_to_time(request)

        if attendance is None:
            if 'emp_in' in request.data.keys():
                employee.attendance_set.create(
                    employee=employee,
                    emp_in=request.data['emp_in'],
                    date=datetime.now().date(),
                    user=request.user
                )
            else:
                raise DoesNotExist(detail="Please enter In time of employee.")
        elif attendance.emp_out is None:
            if 'emp_out' in request.data.keys():
                if request.data['emp_out'] > attendance.emp_in:
                    attendance.emp_out = request.data['emp_out']
                    # attendance.worked_hours = attendance.emp_out.hour - attendance.emp_in.hour
                    attendance.worked_hours = random.randint(1, 10)
                    attendance.save()
                else:
                    raise InvalidFormat(
                        detail="Out time must be greater than In time")
            else:
                raise DoesNotExist(detail="Please enter Out time of employee.")
        elif attendance.emp_in and attendance.emp_out:
            if 'emp_in' in request.data.keys():
                employee.attendance_set.create(
                    employee=employee,
                    emp_in=request.data['emp_in'],
                    date=datetime.now().date(),
                    user=request.user
                )
            else:
                raise DoesNotExist(detail="Please enter In time of employee.")

    def get_attendance_report(self, data):
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
            employee = employee_service.get_hour_base_employee(
                pk=data['employee'])
            attendance = BaseService.serialize_object(
                'AttendanceSerializer',
                employee.attendance_set.filter(
                    date__gte=data['from_date'],
                    date__lte=data['to_date']
                ),
                many=True,
            )
        else:
            attendance = BaseService.serialize_object(
                'AttendanceSerializer',
                self.get_attendance_list().filter(
                    date__gte=data['from_date'],
                    date__lte=data['to_date']
                ),
                many=True,
            )
        return {
            'data': attendance,
            'columns': [
                {
                    'field': "name", 'headerName': "Name", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "emp_in", 'headerName': "In", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "emp_out", 'headerName': "Out", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "worked_hours", 'headerName': "Total hours", 'flex': 1, 'minWidth': 150
                },
                {
                    'field': "date", 'headerName': "Date", 'flex': 1, 'minWidth': 150
                },
            ]
        }
