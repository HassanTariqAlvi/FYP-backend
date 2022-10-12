from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class UserLogoutView(APIView):
    def post(self, request):
        response = Response()
        for cookie in request.COOKIES:
            response.delete_cookie(cookie)
        response.data = {'message': 'You are logged out'}
        response.status_code = status.HTTP_200_OK
        return response
