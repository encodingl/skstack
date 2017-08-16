from django.conf.urls import url
from skapi import views

urlpatterns = [
    url(r'^grafana/$', views.grafana, name='grafana'),
    url(r'^grafana/search$', views.grafana_search, name='grafana_s'),
]