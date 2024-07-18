from django.core.validators import FileExtensionValidator
from django.db import models
from .anime_model import Anime



def episode_path(instance, filename: str):
    if filename.endswith('.mp4'):
        return f"episodes/{instance.anime.id}/{instance.episode_number}.mp4"
    raise ValueError('File must be mp4')


class Episode(models.Model):
    anime = models.ForeignKey(to=Anime, on_delete=models.CASCADE, verbose_name='Аниме')
    episode_number = models.SmallIntegerField(verbose_name='Номер эпизода')
    video = models.FileField(upload_to=episode_path,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             verbose_name='Видео')

    class Meta:
        db_table = 'episode'
        verbose_name = 'Эпизод'
        verbose_name_plural = 'Эпизоды'

    def __str__(self):
        return f"{self.anime.title}; Эпизод - {self.episode_number}"


