from api.serializers.UserGroupSerializer import UserGroupSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import UserGroup
from app.services.PermissionService import PermissionService
from app.services.GroupService import GroupService
from rest_framework.response import Response
from rest_framework.decorators import action
from app.exceptions import AlreadyExists


class GroupView(AbstractBaseView):
    model = UserGroup
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    post_message = "Group created successfully!"
    put_message = "Group updated successfully!"
    delete_message = "Group deleted successfully!"

    def create(self, request, *args, **kwargs):
        permission_service = PermissionService()
        if request.data is not None:
            request.data['permissions'] = permission_service.get_permissions_id(
                request.data['user_permissions'])
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        permission_service = PermissionService()
        request.data['permissions'] = permission_service.get_permissions_id(
            request.data['user_permissions'])
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.validated_data['permissions'] = self.request.data['permissions']
        return self.model.objects.create(**serializer.validated_data)

    def perform_update(self, serializer):
        serializer.validated_data['permissions'] = self.request.data['permissions']
        return self.model.objects.update(**serializer.validated_data)

    @action(detail=True)
    def edit_group(self, request, **kwargs):
        group_service = GroupService()        
        data = group_service.get_edit_group_data(**kwargs)
        return Response(data)

    def perform_destroy(self, instance):
        if instance.user_set.all().count() != 0:
            raise AlreadyExists(
                detail="Users with this group exists. Please remove these users before removing this group")
        return super().perform_destroy(instance)
