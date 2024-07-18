from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.paginator import Paginator

from anime.models.anime_model import Anime
from services.s3_service import S3Service



class ReleaseView(APIView):
    s3 = S3Service()
    def anime_to_dict(self, anime: Anime) -> dict:
        image = anime.image
        if image:
            object_name = image.name
        else:
            object_name = 'others/NotFoundArt.jpg'
        output = {
            'id': anime.id,
            'title': anime.title,
            'slug': anime.slug,
            'description': anime.description[:160] + '...',
            'image_data': ReleaseView.s3.get_url(object_name=object_name),
            'episodes_number': anime.episodes_number,
        }
        return output

    def get(self, request, page_number=1):
        anime_by_popularity = Anime.objects.all().order_by('-favorites_count')
        anime_indexes = [anime.id for anime in anime_by_popularity]

        paginator = Paginator(anime_indexes, 12)
        output_page_indexes = list(paginator.page(page_number))

        anime_list = []
        for anime in anime_by_popularity:
            if anime.id in output_page_indexes:
                anime = self.anime_to_dict(anime)
                anime_list.append(anime)

        output = {
            "pages": paginator.num_pages,
            "anime_list": anime_list
        }
        return Response(output, status=200)