from django.conf.urls import url
from skapi import views

urlpatterns = [
    url(r'^grafana/$', views.grafana, name='grafana'),
    url(r'^grafana/search$', views.grafana_search, name='grafana_s'),
    url(r'^zabbix_sender$', views.zabbix_sender, name='zabbix_sender$'),
    url(r'^get_urllist', views.get_urllist, name='get_urllist'),
]
