from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

from rest_auth.app_settings import TokenSerializer, JWTSerializer, create_token
from rest_auth.models import TokenModel
from rest_auth.utils import jwt_encode
import requests

from .serializers import RegisterSerializer

from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from .providers.google.views import GoogleOAuth2RestAdapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = settings.SITE_PROTOCOL + settings.SITE_DOMAIN
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2RestAdapter
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class RegisterView(CreateAPIView):
    from rest_auth.registration.app_settings import (
        register_permission_classes,
    )

    serializer_class = RegisterSerializer
    permission_classes = register_permission_classes()
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, "REST_USE_JWT", False):
            data = {"user": user, "token": self.token}
            return JWTSerializer(data).data
        else:
            return TokenSerializer(user.auth_token).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response = Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

        if getattr(settings, "REST_USE_JWT", False):
            from rest_framework_jwt.settings import (
                api_settings as jwt_settings,
            )

            if jwt_settings.JWT_AUTH_COOKIE:
                from datetime import datetime

                expiration = (
                    datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
                )
                response.set_cookie(
                    jwt_settings.JWT_AUTH_COOKIE,
                    self.token,
                    expires=expiration,
                    httponly=True,
                )
        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, "REST_USE_JWT", False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user

    def get_response_serializer(self):
        if getattr(settings, "REST_USE_JWT", False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer
