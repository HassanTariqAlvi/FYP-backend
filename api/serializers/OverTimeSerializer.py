from datetime import datetime
from rest_framework import serializers
from app.models import OverTime


class OverTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverTime
        fields = ['id', 'employee', 'start',
                  'end', 'worked_hours', 'date']

        extra_kwargs = {
            "employee": {
                "error_messages": {
                    "invalid": "Please enter employee id",
                    "required": "Please enter employee id",
                    "blank": "Please enter employee id"
                }
            },
            "start": {
                "error_messages": {
                    "invalid": "Please enter start time",
                    "required": "Please enter start time",
                    "blank": "Please enter start time"
                }
            },
            "end": {
                "error_messages": {
                    "invalid": "Please enter end time",
                    "required": "Please enter end time",
                    "blank": "Please enter end time"
                }
            },
            "date": {
                "error_messages": {
                    "invalid": "Please select date of overtime",
                    "required": "Please select date of overtime",
                    "blank": "Please select date of overtime"
                }
            }
        }

    def validate(self, data):
        keys = data.keys()
        if 'date' in keys:
            if data['date'] != datetime.now().date():
                raise serializers.ValidationError('Date must be current date')
        if 'start' in keys and 'end' in keys:
            if data['end'] < data['start']:
                raise serializers.ValidationError(
                    'End time must be greater than Start time')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.employee.name
        representation['employee_data'] = {
            "image": f"http://localhost:8000{instance.employee.image.url}",
            "Name": instance.employee.name,
            "Department": instance.employee.department.name,
            "CNIC": instance.employee.cnic,
            "Phone no": instance.employee.phone_no,
        }
        return representation
