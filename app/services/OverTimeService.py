import random
from datetime import datetime
from app.models import OverTime
from app.exceptions import DoesNotExist, InvalidFormat
from app.services.EmployeeService import EmployeeService


class OverTimeService:
    def get_overtime_list(self):
        return OverTime.objects.all()

    def filter_overtime(self, employee):
        return employee.overtime_set.filter(date=datetime.now().date()).last()

    def save_overtime(self, user,  data):
        data['worked_hours'] = data['end'].hour - data['start'].hour

        OverTime.objects.create(user=user, **data)

    def update_overtime(self, id, user,  data):
        data['worked_hours'] = data['end'].hour - data['start'].hour
        OverTime.objects.update(id, user=user, **data)
