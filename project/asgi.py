"""
ASGI config for planner project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

if "DJANGO_ENV" in os.environ and os.environ["DJANGO_ENV"] == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings-dev")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from .urls import sockets_pattern

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(sockets_pattern),
        # Just HTTP for now. (We can add other protocols later.)
    }
)
