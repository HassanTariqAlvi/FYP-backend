from app.services.BaseService import BaseService
from app.services.PermissionService import PermissionService
from app.models import UserGroup


class GroupService:
    def get_edit_group_data(self, **kwargs):
        permission_service = PermissionService()

        group = UserGroup.objects.get(**kwargs)
        allowed_permissions = permission_service.get_permissions_list(
            group.permissions.all()
        )
        other_permissions = permission_service.exclude_allowed_permissions(
            allowed_permissions, list_format=True)
        return {
            'allowed_permissions': allowed_permissions,
            'other_permissions': other_permissions
        }
