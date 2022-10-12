from rest_framework import serializers
from app.models import LoanDetail
from app.services.BaseService import BaseService


class LoanDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDetail
        fields = ['employee', 'total_loan_left', 'loan_pending']


class LoanDetailReportTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDetail
        fields = ['employee', 'total_loan_left', 'loan_pending']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['id'] = instance.pk
        representation['name'] = instance.employee.name
        representation['department'] = instance.employee.department.name
        representation['phone_no'] = instance.employee.phone_no
        representation['loan_pending'] = "Yes" if instance.loan_pending else "No"
        # representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation


class LoanDetailReportSerializer(serializers.Serializer):
    employee = serializers.IntegerField(required=False)
    employee_selection = serializers.CharField(required=False)

    def validate(self, data):
        if 'employee_selection' not in data.keys():
            raise serializers.ValidationError(
                'Please select One employee or All employees')
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data
