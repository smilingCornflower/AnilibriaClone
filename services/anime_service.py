from anime.models.anime_model import Anime

class AnimeService:
    def __init__(self):
        ...

    def get_sorted(self, key: str) -> list:
        match key:
            case 'updated_at':
                result = Anime.objects.order_by('updated_at')
                return list(result)
            case _:
                raise ValueError("No such key for sorting.")
