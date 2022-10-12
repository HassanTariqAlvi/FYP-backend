from api.validations import validate_positive_number
from app.models import Loan, LoanDetail
from rest_framework import serializers


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'employee',
                  'loan_amount', 'description', 'apply_date', 'status']
        extra_kwargs = {
            "employee": {
                "error_messages": {
                    "null": "Please enter employee id",
                    "incorrect_type": "Employee id must contain only digits"
                }
            },
            "loan_amount": {
                "validators": [validate_positive_number],
                "error_messages": {
                    "invalid": "Please enter loan amount without decimal",
                    "required": "Please enter loan amount without decimal"
                }
            },
            "description": {
                "error_messages": {
                    "blank": "Please enter description",
                    "required": "Please enter description"
                }
            },
            "apply_date": {
                "error_messages": {
                    "blank": "Please select apply date",
                    "required": "Please select apply date"
                }
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['name'] = instance.employee.name
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        representation['employee'] = instance.employee.id
        representation['employee_data'] = {
            "image": f"http://localhost:8000{instance.employee.image.url}",
            "Name": instance.employee.name,
            "Department": instance.employee.department.name,
            "CNIC": instance.employee.cnic,
            "Phone no": instance.employee.phone_no,
        }
        # representation['loan_detail'] = {
        #     # 'Previous loan': instance.employee.loandetail.total_loan_left if Loan.objects.filter(employee=instance.employee).exists() else 0,
        #     'Eligible': 'Yes'
        # }
        return representation
