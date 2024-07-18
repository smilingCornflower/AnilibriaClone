from django.urls import path
from .views.filter_view import FilterView
from .views.other_views import ReleaseView


urlpatterns = [
    path('', ReleaseView.as_view()),
    path('<int:page_number>/', ReleaseView.as_view()),
    path('filter/', FilterView.as_view()),
    path('filter/<int:page_number>/', FilterView.as_view()),
]