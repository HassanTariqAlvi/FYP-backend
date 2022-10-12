from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # exclude = ('groups',)
        extra_kwargs = {
            "employee": {
                "error_messages": {
                    "required": "Please enter employee id",
                },
            },
            "password": {
                "error_messages": {
                    "required": "Please enter password",
                },
            },
            "username": {
                "error_messages": {
                    "required": "Please enter username",
                },
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee_name'] = instance.employee.name if instance.employee else "-"
        if instance.groups.all().count() != 0:
            representation['group'] = instance.groups.all(
            ).first().name if instance.employee else "-"
        else:
            representation['group'] = "Superuser"
        return representation
