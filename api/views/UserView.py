from api.serializers.UserSerializer import UserSerializer
from api.views.AbstractBaseView import AbstractBaseView
from app.models import User
from app.services.EmployeeService import EmployeeService
from app.services.PermissionService import PermissionService
from app.services.UserService import UserService
from rest_framework.decorators import action
from rest_framework.response import Response
from app.exceptions import DoesNotExist


class UserView(AbstractBaseView):
    model = User
    message = 'User'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    post_message = "User registered successfully!"
    put_message = "User information updated successfully!"
    delete_message = "User deleted successfully!"

    user_service = UserService()
    permission_service = PermissionService()

    def create(self, request, *args, **kwargs):
        if request.data is not None and 'user_group' not in request.data.keys():
            raise DoesNotExist(detail='Please select user role')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data is not None and 'user_group' not in request.data.keys():
            raise DoesNotExist(detail='Please select user role')
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        validated_data['user_group'] = self.request.data['user_group']
        return User.objects.update_user(**validated_data)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        validated_data['user_group'] = self.request.data['user_group']
        if 'is_superuser' in validated_data and validated_data['is_superuser'] is True:
            return User.objects.create_superuser(**validated_data)
        else:
            return User.objects.create_user(**validated_data)

    @action(detail=True)
    def add_user(self, request, **kwargs):
        data = self.user_service.get_add_user_data(**kwargs)
        return Response(data)

    @action(detail=True)
    def edit_user(self, request, **kwargs):
        data = self.user_service.get_edit_user_data(**kwargs)
        return Response(data)
