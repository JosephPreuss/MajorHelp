import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import MajorHelp.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pestopanini.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            MajorHelp.routing.websocket_urlpatterns
        )
    ),
})
