from django.conf import settings
from django.urls import path

from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)


urlpatterns = [
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('login/', LoginView.as_view(), name='rest_login'),
]

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
