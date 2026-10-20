import string
from  django.utils.deprecation import MiddlewareMixin
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.core.exceptions import ValidationError

CSRF_TOKEN_LENGTH = 64
CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits
CSRF_AGE_HOURS = 1
CSRF_TOKEN_KEY = "csrftoken4jwt"
EXEMPT_METHODS = ["GET", "HEAD", "OPTIONS", "TRACE"]

class Csrf4JWTMiddleware(MiddlewareMixin):
    """
    This middleware is used to issue a CSRF token
    to be used alongside JWT authentication and API.
    """

    def process_request(self, request):
        """
        This method is to process the request
        before the request reach the view.
        """
        return None

    def process_response(self, request, response):
        """
        This method is to add information to response.
        Or reject.
        """
        
        new_token = self._create_token()
        self._set_csrf2cookie(response=response, csrf_token=new_token)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        For specific views, process something.
        """
        try:
            return self._is_tokenvalid(request)
        except ValidationError as e:
            raise ValidationError(message=e.message,
                                  code=e.code)

    def _set_csrf2cookie(self, response, csrf_token):
        response.set_cookie(key=CSRF_TOKEN_KEY,
                            value=csrf_token,
                            max_age=CSRF_AGE_HOURS*3600,
                            path="/",
                            samesite="Lax")
        return response

    def _is_tokenvalid(self, request):
        if request.method in EXEMPT_METHODS:
            return None
        cookie_token = str(request.COOKIES[CSRF_TOKEN_KEY])
        header_token = str(request.META["HTTP_X_CSRFTOKEN"])
        print("cookie_token: ", cookie_token)
        print("header_token: ", header_token)
        if cookie_token != header_token:
            raise ValidationError(message="CSRF Token is invalid.",
                                  code=403)
        return None

    def _create_token(self):
        return self._get_new_csrf_string()

    def _get_new_csrf_string(self):
        return get_random_string(CSRF_TOKEN_LENGTH, allowed_chars=CSRF_ALLOWED_CHARS)

