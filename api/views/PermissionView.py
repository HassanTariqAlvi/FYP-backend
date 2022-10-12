from api.serializers.PermissionSerializer import PermissionSerializer
from django.contrib.auth.models import Permission
from rest_framework import viewsets
from rest_framework.response import Response
from app.services.PermissionService import PermissionService


class PermissionView(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def list(self, request, *args, **kwargs):
        permission_service = PermissionService()
        return Response({"permissions_list": permission_service.get_permissions_list()})
