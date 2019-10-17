from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import skworkorders.routing



application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            skworkorders.routing.websocket_urlpatterns,

        )
    ),
})
