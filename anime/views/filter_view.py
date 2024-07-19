from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator

from anime.models.anime_model import Anime
from anime.services import anime_to_dict

from urllib.parse import unquote
import json


class FilterView(APIView):
    def get(self, request, page_number: int = 1):
        anime_list = [anime_to_dict(anime=anime, mode='full') for anime in Anime.objects.all()]

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
                'image_url': anime['image_url']
            }
            output_page.append(element)

        output = {
            "pages": paginator.num_pages,
            "anime_list": output_page
        }
        return Response(output)