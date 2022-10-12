from api.validations import validate_name, validate_positive_number
from app.models import MeasureCriteria
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class MeasureCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureCriteria
        fields = ['id', 'name', 'quantity']
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter measure criteria name",
                    "required": "Please enter measure criteria name",
                },
                "validators": [
                    validate_name,
                    UniqueValidator(
                        queryset=MeasureCriteria.objects.all(),
                        message="This criteria already exists",
                        lookup='iexact'
                    )
                ]
            },
            "quantity": {
                "error_messages": {
                    "required": "Please enter quantity",
                    "invalid": "Quantity must contain only digits"
                },
                "validators": [
                    validate_positive_number
                ]
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
