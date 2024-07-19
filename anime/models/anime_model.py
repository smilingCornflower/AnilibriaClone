from django.core.validators import FileExtensionValidator
from django.db import models

from .other_models import Genre, Voice, Timing, Subtitles
from services.s3_service import S3Service
from os import path



SEASON_CHOICES = [
    ('summer', 'лето'),
    ('autumn', 'осень'),
    ('spring', 'весна'),
    ('winter', 'зима'),
]

STATUS_CHOICES = [
    ('ongoing', 'онгоинг'),
    ('completed', 'завершен'),
    ('announcement', 'анонс'),
]

WEEKDAY_CHOICES = [
    ('mon', 'Понедельник'),
    ('tue', 'Вторник'),
    ('wed', 'Среда'),
    ('thu', 'Четверг'),
    ('fri', 'Пятница'),
    ('sat', 'Суббота'),
    ('sun', 'Воскресенье'),
]


def image_path(instance, filename: str):
    if path.splitext(filename)[1] in ['.jpg', '.jpeg']:
        return f"anime_covers/{instance.slug}.jpg"
    raise ValueError('File must be jpg/jpeg')


class Anime(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название [русское]')
    title_latin = models.CharField(max_length=200, unique=True, verbose_name='Название [латинское]')
    slug = models.SlugField(max_length=250, unique=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    year = models.PositiveSmallIntegerField(verbose_name='Год')
    season = models.CharField(max_length=6, choices=SEASON_CHOICES, verbose_name='Сезон')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, verbose_name='Статус озвучки')

    favorites_count = models.PositiveIntegerField(default=0, verbose_name='Количество в любимых')

    new_episode_every = models.CharField(
        max_length=11, blank=True, null=True,
        choices=WEEKDAY_CHOICES, verbose_name='Новый эпизод еженедельно')


    image = models.ImageField(upload_to=image_path,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg'])],
                              verbose_name='Постер')

    genres = models.ManyToManyField(to=Genre, blank=True, related_name='anime_list', verbose_name='Жанры')
    voices = models.ManyToManyField(to=Voice, blank=True, related_name='anime_list', verbose_name='Голоса')
    timing = models.ManyToManyField(to=Timing, blank=True, related_name='anime_list', verbose_name='Тайминг')
    subtitles = models.ManyToManyField(to=Subtitles, blank=True, related_name='anime_list', verbose_name='Субтитры')

    # excluded in admin panel
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'anime'
        verbose_name = 'Аниме'
        verbose_name_plural = 'Аниме'
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = self.image
            image_name = self.image.name
            s3 = S3Service()
            s3.upload_fileobj(file_obj=image, object_name=image_name)
