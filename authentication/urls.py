from django.conf.urls import url
from django.urls import path, include
from .views import RegisterView, GoogleLogin, GithubLogin
from rest_framework_jwt.views import refresh_jwt_token
from importlib import import_module

from allauth.socialaccount import providers

urlpatterns = [
    url(r"^", include("rest_auth.urls")),
    url(r"^refresh/", refresh_jwt_token),
    url(r"^registration/", RegisterView.as_view(), name="register"),
    url(r"^login/google/$", GoogleLogin.as_view(), name="google_login"),
    url(r"^login/github/$", GithubLogin.as_view(), name="github_login"),
    url(
        r"^social/",
        include("allauth.socialaccount.urls"),
        name="socialaccount_signup",
    ),
]

# Provider urlpatterns, as separate attribute (for reusability).
# provider_urlpatterns = []
# for provider in providers.registry.get_list():
#     try:
#         prov_mod = import_module(provider.get_package() + ".urls")
#     except ImportError:
#         continue
#     prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
#     if prov_urlpatterns:
#         provider_urlpatterns += prov_urlpatterns
# urlpatterns += provider_urlpatterns