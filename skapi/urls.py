from django.conf.urls import url
from skapi import views, monitor

urlpatterns = [
    url(r'^grafana/$', views.grafana, name='grafana'),
    url(r'^grafana/search$', views.grafana_search, name='grafana_s'),
    url(r'^zabbix_sender$', views.zabbix_sender, name='zabbix_sender'),
    url(r'^get_urllist', views.get_urllist, name='get_urllist'),
    url(r'^monitor/index', monitor.index, name='monitor_index'),
    url(r'^monitor/userlist', monitor.userlist, name='monitor_userlist'),
    url(r'^monitor/useradd', monitor.useradd, name='monitor_useradd'),
    url(r'^monitor/useredit', monitor.useredit, name='monitor_useredit'),
    url(r'^monitor/grouplist', monitor.grouplist, name='monitor_grouplist'),
    url(r'^monitor/groupadd', monitor.groupadd, name='monitor_grooupadd'),
    url(r'^monitor/groupedit', monitor.groupedit, name='monitor_groupedit'),
    url(r'^monitor/setup', monitor.setuplist, name='monitor_setuplist'),
    url(r'^monitor/setupedit', monitor.setupedit, name='monitor_setupedit'),
]
