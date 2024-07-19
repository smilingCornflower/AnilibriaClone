from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.paginator import Paginator

from anime.models.anime_model import Anime
from anime.models.episode_model import Episode
from anime.services import anime_to_dict
from services.s3_service import S3Service



class ReleaseView(APIView):
    def get(self, request, page_number=1):
        anime_by_popularity = Anime.objects.all().order_by('-favorites_count')
        anime_indexes = [anime.id for anime in anime_by_popularity]

        paginator = Paginator(anime_indexes, 12)
        output_page_indexes = list(paginator.page(page_number))

        anime_list = []
        for anime in anime_by_popularity:
            if anime.id in output_page_indexes:
                anime = anime_to_dict(anime, mode='short')
                anime_list.append(anime)

        output = {
            "pages": paginator.num_pages,
            "anime_list": anime_list
        }
        return Response(output, status=200)



class ScheduleView(APIView):
    def get(self, request):
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        output = {
            day: [
                anime_to_dict(anime, mode='short') for anime in Anime.objects.filter(new_episode_every=day)
            ] for day in weekdays
        }
        return Response(output, status=200)

class AlphabetView(APIView):
    def get(self, request):
        russian_letters = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        anime_list = [anime_to_dict(anime, mode='short') for anime in Anime.objects.all()]
        output = {
            letter: [anime for anime in anime_list if anime['title'][0].upper() == letter]
            for letter in russian_letters
        }
        return Response(output, status=200)