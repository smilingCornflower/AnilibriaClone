from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout



# TODO: Надо сделать все через сериализатор

class LoginView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            response = Response({"message": "User is authenticated"}, status=200)
            response.set_cookie(
                key='test_cookie',
                value='cookie_value',
                httponly=False,
            )
            return response
            # token, created = Token.objects.get_or_create(user=user)

        else:
            return Response(status=404)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=200)