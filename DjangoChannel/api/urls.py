from django.urls import path

from .views import (
    CreateUserView,
    SetTokensCookieView,
    RefreshCookieView,
    DeleteTokenView,
    JWTBaseView,
    get_csrf_token,
)

app_name = 'api'

urlpatterns = [
    path('token/', SetTokensCookieView.as_view(), name="cookies"),
    path('token/refresh/', RefreshCookieView.as_view(), name="token_refresh"),
    path('signup/', CreateUserView.as_view(), name="signup"),
    path('logout/', DeleteTokenView.as_view(), name='logout'),
    path('csrf/', get_csrf_token, name="csrf"),
    path('test/', JWTBaseView.as_view(), name="test"),
]
