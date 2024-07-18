from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator

from anime.models.anime_model import Anime
from anime.models.episode_model import Episode
from services.s3_service import S3Service

from urllib.parse import unquote
import json


class FilterView(APIView):
    s3 = S3Service()
    def anime_to_dict(self, anime: Anime) -> dict:
        image = anime.image
        if image:
            object_name = image.name
        else:
            object_name = 'others/NotFoundArt.jpg'

        episodes_number = Episode.objects.filter(anime=anime).count()
        output = {
            'id': anime.id,
            'title': anime.title,
            'slug': anime.slug,
            'description': anime.description[:160] + '...',
            'episodes_number': episodes_number,
            'year': anime.year,
            'season': anime.season,
            'favorites_count': anime.favorites_count,
            'updated_at': anime.updated_at,
            'status': anime.status,
            'genres': [i.name for i in anime.genres.all()],
            'image_data': FilterView.s3.get_url(object_name=object_name),
        }
        return output

    def get(self, request, page_number: int = 1):
        anime_list = [self.anime_to_dict(anime=anime) for anime in Anime.objects.all()]

        req_data = request.GET.get('data')

        if req_data is not None:
            req_data = json.loads(unquote(req_data))
        else:
            req_data = {}

        if req_data.get('genres'):
            result = []
            for anime in anime_list:
                if all([genre in anime['genres'] for genre in req_data['genres']]):
                    result.append(anime)
            anime_list = result

        if req_data.get('year'):
            anime_list = [anime for anime in anime_list if anime['year'] in req_data['year']]
        if req_data.get('season'):
            anime_list = [anime for anime in anime_list if anime['season'] in req_data['season']]

        if req_data.get('popular_or_new') == 'new':
            anime_list.sort(key=lambda x: x['updated_at'], reverse=True)
        else:  # by popularity
            anime_list.sort(key=lambda x: x['favorites_count'], reverse=True)

        if req_data.get('is_completed'):
            anime_list = [anime for anime in anime_list if anime['status'] in ['completed']]

        paginator = Paginator(anime_list, 12)
        output_page = []
        for anime in paginator.page(page_number):
            element = {
                'id': anime['id'],
                'title': anime['title'],
                'slug': anime['slug'],
                'description': anime['description'],
                'episodes_number': anime['episodes_number'],
                'image_data': anime['image_data']
            }
            output_page.append(element)

        output = {
            "pages": paginator.num_pages,
            "anime_list": output_page
        }
        return Response(output)
