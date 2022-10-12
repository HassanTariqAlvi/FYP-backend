from api.validations import validate_name
from app.models import EmployeeType
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = ['id', 'name']
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter employee category",
                    "required": "Please enter employee category",
                },
                "validators": [
                    validate_name,
                    UniqueValidator(
                        queryset=EmployeeType.objects.all(),
                        message="This employee category already exists",
                        lookup='iexact'
                    )
                ]
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
