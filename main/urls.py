from django.urls import path
from .views import YouTubeVideoView, SidePanelView, IndexView, SearchView


urlpatterns = [
    path('', IndexView.as_view()),
    path('main_page/', YouTubeVideoView.as_view(), name='main_page'),
    path('side_panel/', SidePanelView.as_view(), name='side_panel'),
    path('search/', SearchView.as_view()),
]