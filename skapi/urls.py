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
    url(r'^monitor/policy$', monitor.policy, name='monitor_policy'),
    url(r'^monitor/policyadd', monitor.policyadd, name='monitor_policyadd'),
    url(r'^monitor/policydel', monitor.policydel, name='monitor_policydel'),
    url(r'^monitor/policyedit/(?P<ids>\d+)/$', monitor.policyedit, name='monitor_policyedit'),
    url(r'^monitor/grouplist', monitor.grouplist, name='monitor_grouplist'),
    url(r'^monitor/groupadd', monitor.groupadd, name='monitor_groupadd'),
    url(r'^monitor/groupdel', monitor.groupdel, name='monitor_groupdel'),
    url(r'^monitor/groupedit/(?P<ids>\d+)/$', monitor.groupedit, name='monitor_groupedit'),
    url(r'^monitor/tokenlist', monitor.tokenlist, name='monitor_tokenlist'),
    url(r'^monitor/tokenadd', monitor.tokenadd, name='monitor_tokenadd'),
    url(r'^monitor/tokendel', monitor.tokendel, name='monitor_tokendel'),
    url(r'^monitor/alarmlistedit/(?P<ids>\d+)/$', monitor.alarmlistedit, name='monitor_alarmlistedit'),
    url(r'^monitor/setuplist', monitor.setuplist, name='monitor_setuplist'),
    url(r'^monitor/zabbixalart', monitor.zabbixalart, name='monitor_zabbixalart'),
    url(r'^api/(?P<method>\w+)', monitor.api, name='api'),
]
