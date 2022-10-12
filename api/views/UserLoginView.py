from app.services.AuthenticationService import AuthenticationService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        authentication_service = AuthenticationService()
        response = Response()
        return authentication_service.login(request, response)


class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        response.data = {'message': 'You are logged out'}
        response.status_code = status.HTTP_200_OK
        return response
