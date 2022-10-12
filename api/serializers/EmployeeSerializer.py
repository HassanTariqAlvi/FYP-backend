from api.validations import (validate_city, validate_cnic, validate_name,
                             validate_phone_no)
from app.models import Employee, Role
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class EmployeeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'cnic', 'phone_no', 'gender', 'department',
                  'employee_type', 'role', 'joining_date', 'city', 'address', 'image']
        extra_kwargs = {
            "id": {
                "error_messages": {
                    "invalid": "Please enter employee id"
                }
            },
            "name": {
                "error_messages": {
                    "required": "Please enter employee name",
                    "blank": "Please enter employee name"
                },
                "validators": [validate_name]
            },
            "cnic": {
                "error_messages": {
                    "required": "Please enter CNIC",
                    "blank": "Please enter CNIC",
                },
                "validators": [
                    validate_cnic,
                    UniqueValidator(
                        queryset=Employee.objects.all(),
                        message="Employee with this CNIC already exists",
                        lookup='iexact'
                    )
                ]
            },
            "phone_no": {
                "error_messages": {
                    "blank": "Please enter Phone number",
                    "required": "Please enter Phone number",
                },
                "validators": [validate_phone_no]
            },
            "gender": {
                "error_messages": {
                    "null": "Please select gender",
                    "required": "Please select gender",
                }
            },
            "department": {
                "error_messages": {
                    "null": "Please select department",
                    "required": "Please select department",
                }
            },
            "employee_type": {
                "error_messages": {
                    "null": "Please select employee type",
                    "required": "Please select employee type",
                }
            },
            "joining_date": {
                "error_messages": {
                    "invalid": "Please select joining date",
                    "required": "Please select joining date",
                }
            },
            "city": {
                "error_messages": {
                    "blank": "Please enter city name",
                    "required": "Please enter city name",
                },
                "validators": [validate_city]
            },
            "image": {
                "error_messages": {
                    "blank": "Please select image to upload",
                    "required": "Please select image to upload",
                },
            },
            "address": {
                "error_messages": {
                    "blank": "Please enter address",
                    "required": "Please enter address",
                }
            }
        }

    def validate(self, data):
        if data['employee_type'].name != 'Contract' and 'role' not in data.keys():
            raise serializers.ValidationError('Please select employee role')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['department'] = instance.department.name
        representation['employee_type'] = instance.employee_type.name
        representation['role'] = instance.role.name if instance.role is not None else "-"
        representation['imagePath'] = f"http://localhost:8000{instance.image.url}"
        # representation[
        #     'imagePath'] = f"https://muddassirtahiri.pythonanywhere.com{instance.image.url}"
        return representation
