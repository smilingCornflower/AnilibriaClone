from rest_framework.views import APIView
from rest_framework.response import Response

from services.anime_service import AnimeService
from services.episode_service import EpisodeService
from services.s3_service import S3Service
from .models import YouTubeVideo


class YouTubeVideoView(APIView):
    def get(self, request):
        youtube_videos = YouTubeVideo.objects.all()
        output = []
        s3 = S3Service()
        for youtube_video in youtube_videos:
            if youtube_video.image:
                object_name = youtube_video.image.name
            else:
                object_name = 'others/NotFoundArt.jpg'
            element = {
                "id": youtube_video.id,
                "title": youtube_video.title,
                "url": youtube_video.url,
                # todo: image_data -> image_url
                "image_data": s3.get_url(object_name=object_name)
            }
            output.append(element)

        response = Response(output)
        return response


class SidePanelView(APIView):
    def get(self, request):
        s3 = S3Service()
        last_five_updated_anime = AnimeService().get_sorted(key='updated_at')[-5:]
        output = []
        for anime in last_five_updated_anime:
            image = anime.image
            if image:
                object_name = image.name
            else:
                object_name = 'others/NotFoundArt.jpg'

            element = {
                "id": anime.id,
                "title": anime.title,
                "slug": anime.slug,
                "episodes_number": EpisodeService().get_episodes_number(anime_id=anime.id),
                "description": anime.description,
                "image_data": s3.get_url(object_name=object_name)
            }
            output.append(element)

        return Response(output)

class IndexView(APIView):
    def get(self, request):
        return Response()
