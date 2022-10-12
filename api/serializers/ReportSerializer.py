from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    report_type = serializers.CharField()
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
        return data


class DailyWorkReportSerializer(ReportSerializer):
    employee = serializers.IntegerField(required=False)

    def validate(self, data):
        super().validate(data)
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data


class SalaryReportSerializer(ReportSerializer):
    employee = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)

    def validate(self, data):
        super().validate(data)
        if data['report_type'] == 'Salaries report' and 'status' not in data.keys():
            raise serializers.ValidationError('Please select salary status.')
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data


class AttendanceReportSerializer(ReportSerializer):
    employee = serializers.IntegerField(required=False)

    def validate(self, data):
        super().validate(data)
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data
