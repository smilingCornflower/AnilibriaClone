from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from django.conf import settings
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from ..models import User
import re

from datetime import datetime


@api_view(['GET'])
def activate_account(request, activation_token):
    user = get_object_or_404(User, activation_token=activation_token)

    user.is_active = True
    user.activation_token = None
    user.save()

    return Response(status=200)


def send_activation_email(email, activation_link):
    subject = 'Активация аккаунта'
    message = f'Для активации вашего аккаунта перейдите по ссылке:\n {activation_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)



# regex: only letters, numbers and underscore '_'
USERNAME_REGEX = r'^[\w]+$'


# todo: Надо сделать через сериализатор

class SignupView(APIView):
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (username and email and password):
            return Response(status=452)
        elif not re.match(USERNAME_REGEX, username):
            return Response(status=453)

        try:
            validate_email(email)
        except ValidationError:
            return Response(status=454)

        try:
            validate_password(password)
        except ValidationError:
            return Response(status=455)

        try:
            User.objects.get(username=username)
            return Response(status=456)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            return Response(status=457)
        except User.DoesNotExist:
            pass

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False

            user.activation_token = get_random_string(length=50)
            user.save()
        except Exception as e:
            return Response({"detail", repr(e)}, status=500)

        activation_link = f'localhost:5173/user/activate/{user.activation_token}'
        send_activation_email(email, activation_link)

        return Response(status=200)

# 200: 'Success: activation link has been sent to the email',   for user/signin
# 452: 'Missing required fields',
# 453: 'Invalid username: Username must consist of letters, numbers and underscore',
# 454: 'Invalid email',
# 455: 'Invalid password: Password must not be shorter than six characters',
# 456: 'Such an username already exists',
# 457: 'Such an email already exists',
# 458: 'Passwords do not match',
# 500: 'Something went wrong',