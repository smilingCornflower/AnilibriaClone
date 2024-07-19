from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from rest_framework.response import Response

from services.s3_service import S3Service
from anime.services import anime_to_dict
from users.models import User



class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        user = request.user
        if user:
            s3 = S3Service()
            username = user.username
            email = user.email
            image = User.objects.filter(username=username).first().image

            if image:
                image_name = image.name
            else:
                image_name = 'others/NotFoundArt.jpg'

            image_url = s3.get_url(object_name=image_name)
            favourites = [anime_to_dict(anime, mode='short') for anime in user.favorites.all()]
            in_plans = [anime_to_dict(anime, mode='short') for anime in user.in_plans.all()]
            watched = [anime_to_dict(anime, mode='short') for anime in user.watched.all()]
            discarded = [anime_to_dict(anime, mode='short') for anime in user.discarded.all()]

            output = {
                'username': username,
                'email': email,
                'image_url': image_url,
                'favourites': favourites,
                'in_plans': in_plans,
                'watched': watched,
                'discarded': discarded,
            }
            return Response(output, status=200)
        else:
            return Response(status=401)
