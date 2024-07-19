from .views.signup import SignupView, activate_account
from .views.profile import ProfileView
from .views.login_logout import LoginView, LogoutView

from django.urls import path


urlpatterns = [
    path('', LoginView.as_view()),
    path('login/', LoginView.as_view()),
    path('signup/', SignupView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    # path('update_user/', UpdateUser.as_view()),
    path('activate/<str:activation_token>/', activate_account),
]