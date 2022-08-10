from posts.models import Request
import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User


class log_middleware(object):
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        user = self.get_user_from_auth_header(request)
        try:
            Request.objects.create(user=user,
                                    endpoint=request.path)
        except BaseException as e:
            raise e
        # print('middleware')
        response = self._get_response(request)

        return response

    def get_user_from_auth_header(self, request):
        try:
            auth_keyword, token = get_authorization_header(request).split()
            jwt_header, claims, signature = str(token).split('.')

            try:
                payload = api_settings.JWT_DECODE_HANDLER(token)
                try:
                    user_id = api_settings.JWT_PAYLOAD_GET_USER_ID_HANDLER(payload)

                    if user_id:
                        user = User.objects.get(pk=user_id, is_active=True)
                        return user
                    else:
                        msg = 'Invalid payload'
                        return None
                except User.DoesNotExist:
                    msg = 'Invalid signature'
                    return None

            except jwt.ExpiredSignature:
                msg = 'Signature has expired.'
                return None
            except jwt.DecodeError:
                msg = 'Error decoding signature.'
                return None
        except ValueError:
            return None