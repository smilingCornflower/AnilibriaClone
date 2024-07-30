from django.db import models
from anime.models.anime_model import Anime
from users.models import User

class Comment(models.Model):
    anime = models.ForeignKey(to=Anime, on_delete=models.CASCADE, verbose_name='Аниме')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')

    content = models.TextField(verbose_name='Содержание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.user.username}, к аниме {self.anime.title}: {self.content[:20]}"

