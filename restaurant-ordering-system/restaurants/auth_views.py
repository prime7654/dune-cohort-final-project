from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .auth_rate_limit import (
    AUTH_LOCKOUT_MESSAGE,
    clear_auth_failures,
    is_auth_locked,
    record_auth_failure,
)


class RateLimitedAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        if is_auth_locked(request, username):
            return Response(
                {"detail": AUTH_LOCKOUT_MESSAGE},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            locked = record_auth_failure(request, username)
            if locked:
                return Response(
                    {"detail": AUTH_LOCKOUT_MESSAGE},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        clear_auth_failures(request, user.get_username())
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class RateLimitedTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        if is_auth_locked(request, username):
            return Response(
                {"detail": AUTH_LOCKOUT_MESSAGE},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])
        except Exception as exc:
            locked = record_auth_failure(request, username)
            if locked:
                return Response(
                    {"detail": AUTH_LOCKOUT_MESSAGE},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )
            raise exc

        clear_auth_failures(request, username)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
