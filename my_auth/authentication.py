from utils.tz_datetime import datetime
from datetime import timedelta
from typing import Literal

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired.')
        except Exception as e:
            print(e)
            raise ParseError("JWT parse error occurred.")

        # Get the user from the database
        user_id = payload.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise AuthenticationFailed('User not found')

        user.user_activity.set_last_activity()

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user, _type: Literal["refresh", "access"]):
        # Create the JWT payload
        payload = {
            'user_id': user.pk,
            'exp': int((datetime.now() + timedelta(
                hours=settings.JWT_CONF[f'TOKEN_{_type.upper()}_LIFETIME_HOURS']
            )).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'username': user.username,
            'email': user.email
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def refresh_jwt(cls, refresh: str) -> (str, str):
        try:
            payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        user_id = payload.get('user_id')
        if user_id is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise AuthenticationFailed('User not found')

        return JWTAuthentication.create_jwt(user, "access"), JWTAuthentication.create_jwt(user, "refresh")


    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token