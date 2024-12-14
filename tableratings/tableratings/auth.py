from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

ALLOWED_PATHS = ['/api/login/', 'api/register/']


class CookieJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('Authorization')
        if token is None or request.path in ALLOWED_PATHS:
            return (None, None)
        
        try:
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            user = {'id': user_id}
        except TokenError as e:
            raise AuthenticationFailed('Invalid token')
        
        return (user, None)
    
    def has_permission(self, request, view):
        if request.path in ALLOWED_PATHS:
            return True
        else:
            return bool(request.user and request.user.get('id'))