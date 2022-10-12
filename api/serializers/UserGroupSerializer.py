import api.validations as validations
# from django.contrib.auth.models import Group
from app.models import UserGroup
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserGroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserGroup
        fields = "__all__"
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "blank": "Please enter group name",
                    "required": "Please enter group name",
                },
                "validators": [validations.validate_name,
                               UniqueValidator(
                                   queryset=UserGroup.objects.all(),
                                   message="This group already exists",
                                   lookup='iexact'
                               )]
            },
        }
