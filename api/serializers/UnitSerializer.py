from app.models import Unit
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter unit name",
                    "required": "Please enter unit name",
                },
                "validators": [
                    UniqueValidator(
                        queryset=Unit.objects.all(),
                        message="This unit already exists",
                        lookup='iexact'
                    )
                ]
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
