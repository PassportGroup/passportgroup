import os
from django.conf.urls import url
from django.core.asgi import get_asgi_application

# Import other Channels classes and consumers here.
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator


# Fetch Django ASGI application early to ensure AppRegistry is populated
# before importing consumers and AuthMiddlewareStack that may import ORM
# models.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "passportgroup.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Explicitly set 'http' key using Django's ASGI application.
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
               ''
            )
        )
    )
})