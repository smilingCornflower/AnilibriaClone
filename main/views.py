from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from anime.services import get_aniqueryset, anime_to_dict
from services.s3_service import S3Service
from .models import YouTubeVideo
from .context import context
from urllib.parse import unquote

import json
from services.redis_service import R, EXPIRE_3HOUR


class YouTubeVideoView(APIView):
    def get(self, request):

        hash_name = "main_page"
        redis_output = R.get(hash_name)

        if redis_output:
            redis_output = json.loads(redis_output)
            return Response(redis_output, status=200)

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



        output_json = json.dumps(output, ensure_ascii=False)
        R.set(hash_name, output_json)
        R.expire(hash_name, EXPIRE_3HOUR)

        return Response(output)



class SidePanelView(APIView):
    def get(self, request):

        hash_name = "side_panel"
        redis_output = R.get(hash_name)
        if redis_output:
            redis_output = json.loads(redis_output)
            return Response(redis_output, status=200)

        last_five_updated_anime = get_aniqueryset(order_mode='-updated_at')[:5]
        output = []
        for anime in last_five_updated_anime:
            anime_panel = anime_to_dict(anime, mode='short')
            output.append(anime_panel)

        output_json = json.dumps(output, ensure_ascii=False)
        R.set(hash_name, output_json)
        R.expire(hash_name, EXPIRE_3HOUR)

        return Response(output)


class SearchView(APIView):
    def get(self, request):
        search_title = unquote(request.GET.get('title', ''))
        search_title = search_title.lower()

        all_anime = get_aniqueryset(order_mode='-favorites_count')
        all_titles =[anime_to_dict(anime=anime, mode='short') for anime in all_anime]

        if search_title:
            output = []
            for anidict in all_titles:
                if search_title in anidict['title'].lower():
                    output.append(anidict)
        else:
            output = all_titles

        return Response(output)


class IndexView(APIView):
    def get(self, request):
        return render(request, 'index.html', context={"urls": context})
