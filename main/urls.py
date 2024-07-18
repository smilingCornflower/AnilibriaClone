from django.urls import path
from .views import YouTubeVideoView, SidePanelView, IndexView


urlpatterns = [
    path('', IndexView.as_view()),
    path('main_page/', YouTubeVideoView.as_view(), name='main_page'),
    path('side_panel/', SidePanelView.as_view(), name='side_panel'),
]