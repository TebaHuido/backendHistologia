from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Ignorar la ruta de inicio de sesión
        if request.path == '/api/login/':
            return

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            if token:
                try:
                    payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
                    user = get_user_model().objects.get(id=payload['user_id'])
                    request.user = user
                    print(f"User {user.username} is authenticated")
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, get_user_model().DoesNotExist):
                    print("Invalid token")
                    request.user = None
            else:
                print("No token provided")
                request.user = None
        else:
            print("Invalid authorization header")
            request.user = None

# Agrega este middleware a la configuración de MIDDLEWARE en settings.py