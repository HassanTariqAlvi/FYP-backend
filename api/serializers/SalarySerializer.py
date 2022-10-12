from api.validations import validate_positive_number
from app.models import Salary, SalaryGeneration, LoanDetail, SalarySlip
from app.services.BaseService import BaseService
from rest_framework import serializers
from datetime import datetime


class SalaryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"

    def to_representation(self, instance):
        if instance.paid_by is not None:
            if (instance.paid_by.employee is None):
                paid_by = instance.paid_by.username
            else:
                paid_by = instance.paid_by.employee.name
        else:
            paid_by = '-'

        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['employee_id'] = instance.employee.id
        representation['name'] = instance.employee.name
        representation['paid_by'] = paid_by
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation


class SalaryReportTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"

    def to_representation(self, instance):
        if instance.paid_by is not None:
            if (instance.paid_by.employee is None):
                paid_by = instance.paid_by.username
            else:
                paid_by = instance.paid_by.employee.name
        else:
            paid_by = '-'

        representation = super().to_representation(instance)
        representation['id'] = instance.id
        representation['employee_id'] = instance.employee.id
        representation['name'] = instance.employee.name
        representation['paid_by'] = paid_by
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"

        if SalarySlip.objects.filter(salary=instance).exists():
            salaryslip = SalarySlip.objects.get(salary=instance)
            representation['is_loan_deducted'] = "Yes" if salaryslip.is_loan_deducted else "No"
            representation['deducted_amount'] = salaryslip.loanRecovery.deducted_amount if salaryslip.is_loan_deducted else 0
        else:
            representation['is_loan_deducted'] = "No"
            representation['deducted_amount'] = 0
        representation['total_loan_left'] = instance.employee.loandetail.total_loan_left if LoanDetail.objects.filter(
            employee=instance.employee).exists() else 0
        return representation


class SalaryReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = "__all__"

    def to_representation(self, instance):
        if instance.paid_by is not None:
            if (instance.paid_by.employee is None):
                paid_by = instance.paid_by.username
            else:
                paid_by = instance.paid_by.employee.name
        else:
            paid_by = '-'

        representation = super().to_representation(instance)
        representation['employee_id'] = instance.employee.id
        representation['name'] = instance.employee.name
        representation['paid_by'] = paid_by
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"

        return representation


class SalarySerializer(serializers.Serializer):
    salary = serializers.IntegerField()
    employee = serializers.IntegerField()
    from_date = serializers.DateField(validators=[])
    to_date = serializers.DateField(validators=[])
    total_salary = serializers.IntegerField(validators=[])
    net_salary = serializers.IntegerField(validators=[])
    deducted_amount = serializers.IntegerField(
        required=False,
        validators=[validate_positive_number]
    )
    is_deducted = serializers.BooleanField(required=False)

    def validate(self, data):
        deducted_amount = data['deducted_amount']
        employee = BaseService.get_instance('Employee', pk=data['employee'])
        if hasattr(employee, 'loandetail') and deducted_amount != "":
            if employee.loandetail.total_loan_left < int(deducted_amount):
                raise serializers.ValidationError(
                    f'Your pending loan is Rs {employee.loandetail.total_loan_left}')
            if int(deducted_amount) > data['total_salary']:
                raise serializers.ValidationError(
                    'Loan deduction amount exceeds total salary')
        return data


class GenerateSalarySerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(required=False)

    class Meta:
        model = SalaryGeneration
        fields = "__all__"
        extra_kwargs = {
            "generate_date": {
                "error_messages": {
                    "invalid": "Please select to date",
                    "required": "Please select to date",
                }
            },
        }

    def validate_generate_date(self, value):
        current_date = datetime.now().date()
        # if value.month != current_date.month:
        #     raise serializers.ValidationError(
        #         'Date of previous month cannot be selected')
        if value > current_date:
            raise serializers.ValidationError('Date cannot exceed from today')
        if value.day > 8:
            raise serializers.ValidationError(
                'Salaries can only be generated in 1st week of each month')
            # if Salary.objects.all().count() != 0:
            #     if value <= Salary.objects.all().last().to_date:
            #         raise serializers.ValidationError(
            #             'Date cannot be less than the to date of previously calculated salaries')
        return value


class SalaryReportSerializer(serializers.Serializer):
    month = serializers.CharField(required=False)
    year = serializers.CharField(required=False)
    employee_selection = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

    def validate(self, data):
        if 'month' not in data.keys():
            raise serializers.ValidationError(
                'Please select month')
        if 'year' not in data.keys():
            raise serializers.ValidationError(
                'Please select year')
        if 'employee_selection' not in data.keys():
            raise serializers.ValidationError(
                'Please select One employee or All employees')

        if 'status' not in data.keys():
            raise serializers.ValidationError('Please select salary status.')
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data
