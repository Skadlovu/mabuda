"""
ASGI config for xxxworld project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from stream import routing

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xxxworld.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        routing.websocket_urlpatterns
    ),
})
