from app.models import UnitPrice
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


class UnitPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPrice
        fields = ['id', 'unit', 'department', 'criteria', 'price']
        extra_kwargs = {
            "unit": {
                "error_messages": {
                    "null": "Please select unit name",
                    "required": "Please select unit name",
                },
            },
            "department": {
                "error_messages": {
                    "null": "Please select department",
                    "required": "Please select department",
                },
            },
            "criteria": {
                "error_messages": {
                    "null": "Please select measure criteria",
                    "required": "Please select measure criteria",
                },
            },
            "price": {
                "error_messages": {
                    "invalid": "Please enter valid price",
                },
            }
        }
        validators = [
            UniqueTogetherValidator(
                queryset=UnitPrice.objects.all(),
                fields=("unit", 'department', 'criteria'),
                message="Unit price with this department, criteria and name is already created"
            )
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['unit'] = instance.unit.name
        representation['department'] = instance.department.name
        representation['criteria'] = instance.criteria.name
        representation['quantity'] = instance.criteria.quantity
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation
