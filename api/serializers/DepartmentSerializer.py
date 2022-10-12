import api.validations as validations
from app.models import Department
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter department name",
                    "required": "Please enter department name",
                },
                "validators": [
                    validations.validate_name,
                    UniqueValidator(
                        queryset=Department.objects.all(),
                        message="This department already exists",
                        lookup='iexact'
                    )
                ]
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
