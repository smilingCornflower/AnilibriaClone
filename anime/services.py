from anime.models.anime_model import Anime
from anime.models.episode_model import Episode
from services.s3_service import S3Service


def anime_to_dict(anime: Anime, mode: str) -> dict:
    '''
    :param anime: Anime object
    :return: Dictionary with full information about anime
    '''

    s3 = S3Service()

    episode_number = 1
    episode = Episode.objects.filter(anime=anime, episode_number=episode_number).first()
    episodes_number = Episode.objects.filter(anime=anime).count()

    try:
        episode_name = episode.video.name
        episode_url = s3.get_url(object_name=episode_name)
    except AttributeError as err:
        episode_url = ''


    image = anime.image
    if image:
        object_name = image.name
    else:
        object_name = 'others/NotFoundArt.jpg'


    output = {
        'id': anime.id,
        'title': anime.title,
        'title_latin': anime.title_latin,
        'slug': anime.slug,
        'description': anime.description,
        'episodes_number': episodes_number,
        'image_url': s3.get_url(object_name=object_name),
    }
    if mode == 'short':
        return output
    elif mode == 'full':
        output |= {
            'year': anime.year,
            'season': anime.season,
            'favorites_count': anime.favorites_count,
            'status': anime.status,

            'genres': [i.name for i in anime.genres.all()],
            'voices': [i.name for i in anime.voices.all()],
            'timings': [i.name for i in anime.timing.all()],
            'subtitles': [i.name for i in anime.subtitles.all()],

            'episode_url': episode_url if episodes_number else '',
            'episode_number': episode_number,
        }
        return output


def get_anilist(order_mode: str) -> list:
    ordering_args = ['updated_at', '-updated_at']
    if order_mode in ordering_args:
        result = Anime.objects.order_by(order_mode)
        return list(result)
    else:
        raise ValueError("No such ordering")


def get_aniqueryset(order_mode: str):
    ordering_args = ['updated_at', '-updated_at']
    if order_mode in ordering_args:
        result = Anime.objects.order_by(order_mode)
        return result
    else:
        raise ValueError("No such ordering")


def get_episodes_number(anime_id: int) -> int:
    try:
        episodes_count = Episode.objects.filter(anime__id=anime_id).count()
    except Exception:
        return 0
    return episodes_count