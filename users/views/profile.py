from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView

from rest_framework.response import Response

from services.s3_service import S3Service
from anime.services import anime_to_dict, get_anime_by_id
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

    def put(self, request):
        s3 = S3Service()
        user = request.user
        action = request.data.get('action')
        image = request.data.get('image')
        anime_id = request.data.get('anime_id')

        action_commands = {
            'add_to_favorites': lambda anime: user.favorites.add(anime),
            'add_to_plans': lambda anime: user.in_plans.add(anime),
            'add_to_watched': lambda anime: user.watched.add(anime),
            'add_to_discarded': lambda anime: user.discarded.add(anime),
        }

        if action == 'add_image' and image:
            image_name = f"user_image/{user.id}_avatar.jpg"
            image_type = image.content_type
            if image_type in ['image/jpeg', 'image/png', 'image/webp']:
                s3.upload_fileobj(file_obj=image, object_name=image_name)
                user.image.name = image_name
                user.save()
            else:
                return Response(status=400)
        elif action in action_commands:
            if not anime_id:
                return Response({"detail": "Anime id was not provided"}, status=400)
            anime = get_anime_by_id(anime_id=anime_id)

            if not anime:
                return Response({"detail": "Anime was not found"}, status=404)

            action_function = action_commands[action]
            action_function(anime)
        else:
            return Response({"detail": "No such action"}, status=400)
        return Response(status=200)

    def delete(self, request):
        s3 = S3Service()
        user = request.user
        action = request.data.get('action')
        anime_id = request.data.get('anime_id')

        action_commands = {
            'remove_from_favorites': lambda anime: user.favorites.remove(anime),
            'remove_from_plans': lambda anime: user.in_plans.remove(anime),
            'remove_from_watched': lambda anime: user.watched.remove(anime),
            'remove_from_discarded': lambda anime: user.discarded.remove(anime),
        }
        if action == 'delete_image':
            try:
                image_name = user.image.name
                s3.delete_file(object_name=image_name)
            except AttributeError:
                pass  # user has no image
        elif action in action_commands:
            if not anime_id:
                return Response({"detail": "Anime id was not provided"}, status=400)
            anime = get_anime_by_id(anime_id=anime_id)

            if not anime:
                return Response({"detail": "Anime was not found"}, status=404)

            action_function = action_commands[action]
            action_function(anime)

        else:
            return Response({"detail": "No such action"}, status=400)
        return Response(status=200)
