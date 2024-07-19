from django.urls import path
from .views.filter_view import FilterView
from .views.other_views import ReleaseView, ScheduleView, AlphabetView
from .views.watch_views import WatchView, WatchEpisodeView, RandomWatchView


urlpatterns = [
    path('', ReleaseView.as_view()),
    path('<int:page_number>/', ReleaseView.as_view()),
    path('filter/', FilterView.as_view()),
    path('filter/<int:page_number>/', FilterView.as_view()),

    path('schedule/', ScheduleView.as_view()),
    path('alphabet/', AlphabetView.as_view()),

    path('watch/random/', RandomWatchView.as_view()),
    path('watch/<int:anime_id>/', WatchView.as_view()),
    path('watch/<slug:anime_slug>/', WatchView.as_view()),
    path('watch/<int:anime_id>/<int:episode_number>/', WatchEpisodeView.as_view()),
    path('watch/<slug:anime_slug>/<int:episode_number>/', WatchEpisodeView.as_view()),
]