from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import skworkorders.ws_routing
from skworkorders.ws_consumers import pretask



application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            skworkorders.ws_routing.websocket_urlpatterns,

        )
    ),
})
