from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from anime.services import get_aniqueryset, anime_to_dict
from services.s3_service import S3Service
from .models import YouTubeVideo
from .context import context


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
                "image_url": s3.get_url(object_name=object_name)
            }
            output.append(element)

        response = Response(output)
        return response


class SidePanelView(APIView):
    def get(self, request):
        last_five_updated_anime = get_aniqueryset(order_mode='-updated_at')[:5]
        output = []
        for anime in last_five_updated_anime:
            anime_panel = anime_to_dict(anime, mode='short')
            output.append(anime_panel)

        return Response(output)

class IndexView(APIView):
    def get(self, request):
        return render(request, 'index.html', context={"urls": context})
