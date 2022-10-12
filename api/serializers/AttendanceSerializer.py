from rest_framework import serializers
from app.models import Attendance


class AttendanceSerializer(serializers.Serializer):
    # employee = serializers.IntegerField()
    emp_in = serializers.TimeField(required=False)
    emp_out = serializers.TimeField(required=False)
    date = serializers.DateField(required=False)

    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'emp_in',
                  'emp_out', 'worked_hours', 'date']

        extra_kwargs = {
            "employee": {
                "error_messages": {
                    "invalid": "Please enter employee id",
                    "required": "Please enter employee id",
                    "blank": "Please enter employee id"
                }
            }
        }

    def validate(self, data):
        if 'emp_in' not in data.keys():
            raise serializers.ValidationError('Please enter In time')
        if 'emp_out' not in data.keys():
            raise serializers.ValidationError('Please enter out time')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['worked_hours'] = instance.worked_hours
        representation['name'] = instance.employee.name
        return representation


class AttendanceReportSerializer(serializers.Serializer):
    employee = serializers.IntegerField(required=False)
    report_days = serializers.CharField(required=False)
    employee_selection = serializers.CharField(required=False)
    to_date = serializers.DateField(required=False)
    from_date = serializers.DateField(required=False)

    def validate(self, data):
        if 'report_days' not in data.keys():
            raise serializers.ValidationError('Please select days range')
        if 'employee_selection' not in data.keys():
            raise serializers.ValidationError(
                'Please select One employee or All employees')

        if data['report_days'] == 'Custom' and 'from_date' not in data.keys() and 'to_date' not in data.keys():
            raise serializers.ValidationError(
                'Please select from and to date.')
        if data['report_days'] == 'Custom' and data['to_date'] < data['from_date']:
            raise serializers.ValidationError(
                'From date must be smaller than the To date.')
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data
