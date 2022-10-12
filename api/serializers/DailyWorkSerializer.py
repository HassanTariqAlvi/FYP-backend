from rest_framework import serializers
from app.models import DailyWork, Employee, UnitPrice


class DailyWorkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWork
        fields = ['id', 'unit_price', 'date', 'total_pieces',
                  'price_per_unit', 'total_amount']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['employee_name'] = instance.employee.name
        representation['price_per_unit'] = round(instance.price_per_unit, 2)
        representation['unit_name'] = instance.unit_price.unit.name
        representation['user'] = instance.user.employee.name if instance.user.employee else "Admin"
        return representation


class DailyWorkSerializer(serializers.Serializer):
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        error_messages={
            'invalid': 'Please enter employee id',
            'blank': 'Please enter employee id',
            'required': 'Please enter employee id'
        }
    )
    unit = serializers.CharField(
        error_messages={
            'null': 'Please select unit',
            'invalid': 'Please select unit',
            'required': 'Please select unit',
        }
    )
    criteria = serializers.CharField(
        error_messages={
            'null': 'Please select criteria',
            'invalid': 'Please select criteria',
            'required': 'Please select criteria',
        }
    )
    total_pieces = serializers.IntegerField(
        error_messages={
            'invalid': 'Please enter total pieces quantity',
            'required': 'Please enter total pieces quantity',
        }
    )
    unit_price = serializers.PrimaryKeyRelatedField(
        queryset=UnitPrice.objects.all(),
    )
    department = serializers.CharField()
    price_per_unit = serializers.FloatField(required=False)
    total_amount = serializers.IntegerField(required=False)
    date = serializers.DateField()


class DailyWorkReportSerializer(serializers.Serializer):
    employee = serializers.IntegerField(required=False)
    report_days = serializers.CharField(required=False)
    employee_selection = serializers.CharField(required=False)
    to_date = serializers.DateField(required=False)
    from_date = serializers.DateField(required=False)

    def validate(self, data):
        if 'report_days' not in data.keys():
            raise serializers.ValidationError('Please select days range')
        if 'employee_selection' not in data.keys():
            raise serializers.ValidationError(
                'Please select One employee or All employees')

        if data['report_days'] == 'Custom' and 'from_date' not in data.keys() and 'to_date' not in data.keys():
            raise serializers.ValidationError(
                'Please select from and to date.')
        if data['report_days'] == 'Custom' and data['to_date'] < data['from_date']:
            raise serializers.ValidationError(
                'From date must be smaller than the To date.')
        if data['employee_selection'] == 'One employee' and 'employee' not in data.keys():
            raise serializers.ValidationError('Please enter employee id')
        return data
