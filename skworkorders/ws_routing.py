from django.conf.urls import url
from skworkorders.ws_consumers import pretask

websocket_urlpatterns = [
    url(r'^/ws/skworkorders/WorkOrderCommit/pretask/$', pretask),
]
