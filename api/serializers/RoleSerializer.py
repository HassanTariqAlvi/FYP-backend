import api.validations as validations
from app.models import Role
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'salary']
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter role name",
                    "required": "Please enter role name",
                },
                "validators": [validations.validate_name,
                               UniqueValidator(
                                   queryset=Role.objects.all(),
                                   message="This role already exists",
                                   lookup='iexact'
                               )]
            },
            "salary": {
                "error_messages": {
                    "blank": "Please enter salary",
                    "required": "Please enter salary",
                },
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
