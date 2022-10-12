from app.models import LoanRecovery
from app.services.BaseService import BaseService
from rest_framework import serializers


class LoanRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecovery
        fields = ['id', 'loanDetail', 'deducted_amount', 'recovery_date']
        extra_kwargs = {
            "deducted_amount": {
                "error_messages": {
                    "invalid": "Amount must be without decimal",
                    "required": "Please enter amount to be deducted",
                }
            },
            "recovery_date": {
                "error_messages": {
                    "invalid": "Please select recovery date",
                    "required": "Please select recovery date",
                }
            },
        }

    def validate(self, data):
        loanDetail = data['loanDetail']
        if data['deducted_amount'] > loanDetail.total_loan_left:
            raise serializers.ValidationError(
                f'Your pending loan is {loanDetail.total_loan_left}')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employee = BaseService.get_instance(
            'Employee', pk=instance.loanDetail.pk)
        representation['name'] = employee.name
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation


class LoanRecoveryReportTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecovery
        fields = ['id', 'loanDetail', 'deducted_amount', 'recovery_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        employee = BaseService.get_instance(
            'Employee', pk=instance.loanDetail.pk)

        representation['name'] = employee.name
        representation['department'] = employee.department.name
        representation['phone_no'] = employee.phone_no
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation


class LoanRecoveryReportSerializer(serializers.Serializer):
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
