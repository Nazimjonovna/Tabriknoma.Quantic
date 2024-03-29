from django.conf import settings

from dj_rest_auth.serializers import JWTSerializer as DefaultJWTSerializer
from dj_rest_auth.serializers import (
    JWTSerializerWithExpiration as DefaultJWTSerializerWithExpiration,
)
from dj_rest_auth.serializers import LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.serializers import (
    PasswordChangeSerializer as DefaultPasswordChangeSerializer,
)
from dj_rest_auth.serializers import (
    PasswordResetConfirmSerializer as DefaultPasswordResetConfirmSerializer,
)
from dj_rest_auth.serializers import (
    PasswordResetSerializer as DefaultPasswordResetSerializer,
)
from dj_rest_auth.serializers import TokenSerializer as DefaultTokenSerializer
from dj_rest_auth.serializers import (
    UserDetailsSerializer as DefaultUserDetailsSerializer,
)

from .utils import default_create_token, import_callable

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'path.to.custom.LoginSerializer',
    'TOKEN_SERIALIZER': 'path.to.custom.TokenSerializer',
}


create_token = import_callable(getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))

serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})

TokenSerializer = import_callable(serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))

JWTSerializer = import_callable(serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))

JWTSerializerWithExpiration = import_callable(serializers.get('JWT_SERIALIZER_WITH_EXPIRATION', DefaultJWTSerializerWithExpiration))

UserDetailsSerializer = import_callable(serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer))

LoginSerializer = import_callable(serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer))

PasswordResetSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_SERIALIZER', DefaultPasswordResetSerializer,
    ),
)

PasswordResetConfirmSerializer = import_callable(
    serializers.get(
        'PASSWORD_RESET_CONFIRM_SERIALIZER', DefaultPasswordResetConfirmSerializer,
    ),
)

PasswordChangeSerializer = import_callable(
    serializers.get('PASSWORD_CHANGE_SERIALIZER', DefaultPasswordChangeSerializer),
)

JWT_AUTH_COOKIE = getattr(settings, 'JWT_AUTH_COOKIE', None)
JWT_AUTH_REFRESH_COOKIE = getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', None)
