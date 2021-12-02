import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import CustomGoogleProvider


class GoogleOAuth2RestAdapter(OAuth2Adapter):
    provider_id = CustomGoogleProvider.id
    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    token_url = "https://www.googleapis.com/oauth2/v1/tokeninfo"

    def complete_login(self, request, app, token, **kwargs):
        print("rest-auth api")
        # /api/rest-auth/google
        # but not for website login with google
        resp = requests.get(
            self.token_url, params={"id_token": token.token, "alt": "json"}
        )
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider().sociallogin_from_response(
            request, extra_data
        )
        return login


oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2RestAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(GoogleOAuth2RestAdapter)