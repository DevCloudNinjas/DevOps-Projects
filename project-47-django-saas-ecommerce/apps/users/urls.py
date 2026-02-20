from django.urls import path
from .views import RegistrationView, LoginView, LogoutView,ChangePasswordView
from rest_framework_simplejwt import views as jwt_views

app_name = 'users'

urlpatterns = [
    path('users/register', RegistrationView.as_view(), name='register'),
    path('users/login', LoginView.as_view(), name='register'),
    path('users/logout', LogoutView.as_view(), name='register'),
    path('users/change-password', ChangePasswordView.as_view(), name='register'),
    path('users/token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]