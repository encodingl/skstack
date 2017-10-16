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
    url(r'^monitor/userdel', monitor.userdel, name='monitor_userdel'),
    url(r'^monitor/useredit/(?P<ids>\d+)/$', monitor.useredit, name='monitor_useredit'),
    url(r'^monitor/grouplist', monitor.grouplist, name='monitor_grouplist'),
    url(r'^monitor/groupadd', monitor.groupadd, name='monitor_groupadd'),
    url(r'^monitor/groupdel', monitor.groupdel, name='monitor_groupdel'),
    url(r'^monitor/groupedit/(?P<ids>\d+)/$', monitor.groupedit, name='monitor_groupedit'),
    url(r'^monitor/alarmlistedit/(?P<ids>\d+)/$', monitor.alarmlistedit, name='monitor_alarmlistedit'),
    url(r'^monitor/setuplist', monitor.setuplist, name='monitor_setuplist'),
    url(r'^monitor/setupedit', monitor.setupedit, name='monitor_setupedit'),
    url(r'^monitor/zabbixalart', monitor.zabbixalart, name='monitor_zabbixalart'),
]
