"""planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from main.views import LogAdd
from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from main.utils import includeSockets

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from channels.routing import URLRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from django.urls import re_path
from rest_framework_cache.registry import cache_registry

cache_registry.autodiscover()
schema_view = get_schema_view(
    openapi.Info(
        title="Planner API",
        default_version="v1",
        description="Planner API Docs",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^admin/defender/", include("defender.urls")),
    path("api/log", LogAdd.as_view()),
    path("api/auth/", include("authentication.urls")),
    path("api/users/", include("users.urls")),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-open",
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    url(
        r"^api/docs/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="c-schema",
    ),
]

sockets_pattern = URLRouter([])

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

if settings.DEBUG is False:
    urlpatterns += [url("api/prometheus/", include("django_prometheus.urls"))]
