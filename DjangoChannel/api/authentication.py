from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from django.utils.translation import gettext_lazy as _

class CustomJWTAuthentication(JWTAuthentication):
    """
    This class is for an HttpOnly cookie.
    To look at JWT tokens set in cookie.
    """

    def authenticate(self, request):
        """
        Return a 'User' if a correct JWT token has been supplied.
        """
        raw_access_token = self.get_raw_access_token(request)
        if raw_access_token is None:
             return None
        validated_token = self.get_validated_token(raw_access_token)
        return self.get_user(validated_token), validated_token

    def get_raw_access_token(self, request):
        """
        Obtain an access jwt token from cookie.
        """

        try:
            raw_access_token = request.COOKIES["access"]
        except KeyError:
            raise AuthenticationFailed(
                _("There isn't access token in cookie. Please refresh a token."),
                code="refresh_required",
            )

        return raw_access_token
        

    def get_validated_token(self, raw_token):
        """
        convert a raw access token to a Token object.
        We can now retrieve information such as the expiry date.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": messages,
            }
        )


    def get_user(self, validated_token):
        """
        return an user object
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError as e:
            raise InvalidToken(
                _("Token contained no recognizable user identification")
            ) from e

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist as e:
            raise AuthenticationFailed(
                _("User not found"), code="user_not_found"
            ) from e

        if api_settings.CHECK_USER_IS_ACTIVE and not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user
