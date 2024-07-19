from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('release/', include('anime.urls')),
    path('user/', include('users.urls')),
]
