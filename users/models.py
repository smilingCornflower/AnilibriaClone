from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from anime.models.anime_model import Anime
from datetime import datetime
from os import path




def avatar_path(instance, filename: str):
    base_name, file_type = path.splitext(filename)
    date_of_upload = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    if file_type in ['.jpg', '.jpeg', '.png', '.webp']:
        return f"user_image/{instance.username}_avatar_{date_of_upload}.jpg"
    else:
        raise ValueError("Incorrect filetypes")



class User(AbstractUser):
    image = models.ImageField(upload_to=avatar_path, validators=[FileExtensionValidator(['jpg', 'jpeg', 'webp', 'png'])],
                              null=True, blank=True, verbose_name='Аватар')

    favorites = models.ManyToManyField(to=Anime, related_name='favorited_by', blank=True, verbose_name='Любимые аниме')
    in_plans = models.ManyToManyField(to=Anime,  related_name='planned_by', blank=True, verbose_name='В планах')
    watched = models.ManyToManyField(to=Anime,  related_name='watched_by', blank=True, verbose_name='Просмотрено')
    discarded = models.ManyToManyField(to=Anime,  related_name='discarded_by', blank=True, verbose_name='Брошено')

    activation_token = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
