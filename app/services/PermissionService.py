from django.contrib.auth.models import Permission


class PermissionService:

    def get_all_permissions(self):
        return Permission.objects.all()

    def get_permissions_list(self, queryset=None):
        permissions_list = []
        if queryset is None:
            queryset = self.get_all_permissions()
        for row in queryset:
            permissions_list.append(row.name)
        return permissions_list

    def exclude_allowed_permissions(self, allowed_permissions, list_format):
        permissions = Permission.objects.exclude(name__in=allowed_permissions)
        if list_format:
            return self.get_permissions_list(permissions)
        return permissions

    def get_permissions_id(self, permissions_list):
        if permissions_list is None:
            queryset = self.get_all_permissions()
        queryset = Permission.objects.filter(name__in=permissions_list)
        return [row.id for row in queryset]
