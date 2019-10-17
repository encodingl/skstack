from django.conf.urls import url
from django.urls import path
from skworkorders.WorkOrderConsumer import pretask



websocket_urlpatterns = [
    path('ws/skworkorders/WorkOrderCommit/pretask/', pretask),

]
