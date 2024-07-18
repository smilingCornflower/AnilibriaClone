from anime.models.episode_model import Episode


class EpisodeService:
    def __init__(self):
        ...

    def get_episodes_number(self, anime_id: int) -> int:
        episodes_count = Episode.objects.filter(anime__id=anime_id).count()
        return episodes_count