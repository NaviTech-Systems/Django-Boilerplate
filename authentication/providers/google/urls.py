from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import CustomGoogleProvider


urlpatterns = default_urlpatterns(CustomGoogleProvider)
