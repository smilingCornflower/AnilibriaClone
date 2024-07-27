from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from anime.models.anime_model import Anime
from anime.models.episode_model import Episode
from anime.services import anime_to_dict

from services.s3_service import s3

from random import choice
import json
from services.redis_service import R, EXPIRE_10MIN


class WatchView(APIView):
    def get(self, request, anime_slug: str):
        hash_name = f'watch_{anime_slug}'
        redis_output = R.get(hash_name)
        if redis_output:
            redis_output = json.loads(redis_output)
            return Response(redis_output, status=200)

        anime = get_object_or_404(Anime, slug=anime_slug)
        anime_info = anime_to_dict(anime, mode='full')

        anime_info_json = json.dumps(anime_info, ensure_ascii=False)
        R.set(hash_name, anime_info_json)
        R.expire(hash_name, EXPIRE_10MIN)

        return Response(anime_info, status=200)


class WatchEpisodeView(APIView):
    def get(self, request, anime_slug: str, episode_number: int):

        episode = Episode.objects.filter(anime__slug=anime_slug, episode_number=episode_number).first()
        try:
            episode_name = episode.video.name
            episode_url = s3.get_url(object_name=episode_name)
        except AttributeError as e:
            return Response({"detail": repr(e)}, status=404)

        output = {
            "episode_url": episode_url,
            "episode_number": episode_number,
        }
        return Response(output, status=200)


class RandomWatchView(APIView):
    def get(self, request):
        random_anime = choice(Anime.objects.all())
        anime_info = anime_to_dict(random_anime, mode='full')
        return Response(anime_info, status=200)