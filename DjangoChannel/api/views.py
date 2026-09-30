from wsgiref.handlers import format_date_time

from rest_framework import generics
from rest_framework import views

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt import tokens as jwt_tokens
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from django.contrib.auth import get_user_model

from .serializers import (
    CustomUserSerializer,
    LoginSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return SetTokensCookieView.as_view()(request._request)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SetTokensCookieView(jwt_views.TokenObtainPairView):

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]

        decoded_access_token = jwt_tokens.AccessToken(access_token)
        decoded_refresh_token = jwt_tokens.RefreshToken(refresh_token)

        exp_access_token = format_date_time(decoded_access_token["exp"])
        exp_refresh_token = format_date_time(decoded_refresh_token["exp"])

        res = Response(status=status.HTTP_200_OK)

        res.set_cookie(key="access",
                       value=access_token,
                       expires=exp_access_token,
                       httponly=True)
        res.set_cookie(key="refresh",
                       value=refresh_token,
                       expires=exp_refresh_token,
                       httponly=True)

        return res


class RefreshCookieView(jwt_views.TokenRefreshView):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):

        refresh_token = request.COOKIES.get("refresh", None)

        if refresh_token is None:
            raise InvalidTokenError("You do not have a refresh token.")

        token_data = {
            "refresh": refresh_token,
        }
        serializer = self.get_serializer(data=token_data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        access_token = serializer.validated_data["access"]
        decoded_access_token = jwt_tokens.AccessToken(access_token)
        exp_access_token = format_date_time(decoded_access_token["exp"])
        res = Response(status=status.HTTP_200_OK)
        res.set_cookie(key="access",
                       value=access_token,
                       expires=exp_access_token,
                       httponly=True)
        return res


class DeleteTokenView(views.APIView):

    http_method_names = ["get"]
    
    def get(self, request, *args, **kwargs):
        res = Response(status=status.HTTP_200_OK)
        res.delete_cookie(key="refresh")
        res.delete_cookie(key="access")
        return res
