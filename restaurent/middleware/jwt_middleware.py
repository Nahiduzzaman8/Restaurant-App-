import jwt
from django.conf import settings
from django.contrib.auth.models import User
from baseapp.jwt_utils import decode_jwt

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        token = request.COOKIES.get("jwt")
        request.user = None

        if token:
            payload = decode_jwt(token)
            if payload:
                try:
                    user = User.objects.get(id=payload["user_id"])
                    request.user = user
                except User.DoesNotExist:
                    pass

        return self.get_response(request)
