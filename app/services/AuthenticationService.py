from app.exceptions import AccessDenied, AuthenticationFailed
from django.conf import settings
from django.contrib.auth import authenticate
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationService:
    def __get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __get_user_permissions(self, app_name, user):
        _dict = {}
        # if user.employee is None:
        #     permissions = user.get_user_permissions()
        #     if len(permissions) != 0:
        #         for name in permissions:
        #             start = name.index('.')
        #             end = name.index('_')
        #             model = name[end+1:]
        #             if model not in _dict:
        #                 _dict[model] = []
        #             _dict[model].append(name[start+1:end])
        # else:
        #     permissions = user.groups.all().first().permissions.all()
        #     if len(permissions) != 0:
        #         for name in permissions:
        #             operation, model = name.codename.split('_')
        #             if model not in _dict:
        #                 _dict[model] = []
        #             _dict[model].append(operation)

        permissions = user.get_user_permissions()
        if len(permissions) != 0:
            for name in permissions:
                start = name.index('.')
                end = name.index('_')
                model = name[end+1:]
                if model not in _dict:
                    _dict[model] = []
                _dict[model].append(name[start+1:end])
        return _dict

    def login(self, request, response):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active and user.is_staff:
                permissions = self.__get_user_permissions('app', user)
                token = self.__get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=token["access"],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                )
                csrf.get_token(request)
                response.data = {
                    'logged_in': True,
                    'is_superuser': user.is_superuser,
                    'user': user.employee.name if user.employee else "Admin",
                    'permissions': permissions,
                    'access_token': token['access'],
                    'refresh_token': token['refresh'],
                }
                return response
            else:
                raise AccessDenied(
                    detail="You have been blocked by the administrator to access the system."
                )
        else:
            raise AuthenticationFailed(
                detail='Invalid email or password. OR Contact with administrator.'
            )
