from api.serializers.RoleSerializer import RoleSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import Role
from app.services.BaseService import BaseService


class RoleView(AbstractBaseView):
    model = Role
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    post_message = "Role created successfully!"
    put_message = "Role updated successfully!"
    delete_message = "Role deleted successfully!"

    # def create(self, request, *args, **kwargs):
    #     if request.data is not None:
    #         keys = request.data.keys()
    #         if 'employee_type' in keys:
    #             request.data['employee_type'] = BaseService.get_instance(
    #                 'EmployeeType', name=request.data['employee_type']
    #             ).id
    #     return super().create(request, *args, **kwargs)
