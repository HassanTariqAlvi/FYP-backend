from rest_framework import serializers
from app.models import ReversionVersion


class LogFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReversionVersion
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_created'] = instance.revision.date_created
        representation['comment'] = instance.revision.comment
        representation['Created_by'] = instance.revision.user.employee.name if instance.revision.user.employee else "-"
        return representation
