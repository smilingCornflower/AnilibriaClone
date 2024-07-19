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
            # token, created = Token.objects.get_or_create(user=user)
            return Response(status=200)

        else:
            return Response(status=404)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=200)