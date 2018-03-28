from django.conf.urls import url
from skapi import views, monitor

urlpatterns = [
    url(r'^grafana/$', views.grafana, name='grafana'),
    url(r'^grafana/search$', views.grafana_search, name='grafana_s'),
    url(r'^zabbix_sender$', views.zabbix_sender, name='zabbix_sender'),
    url(r'^get_urllist', views.get_urllist, name='get_urllist'),
    url(r'^monitor/index', monitor.index, name='monitor_index'),
    url(r'^monitor/policy$', monitor.policy, name='monitor_policy'),
    url(r'^monitor/policyadd', monitor.policyadd, name='monitor_policyadd'),
    url(r'^monitor/policydel', monitor.policydel, name='monitor_policydel'),
    url(r'^monitor/policyedit/(?P<ids>\d+)/$', monitor.policyedit, name='monitor_policyedit'),
    url(r'^monitor/servicetype$', monitor.servicetype, name='monitor_servicetype'),
    url(r'^monitor/servicetypeeadd', monitor.servicetypeadd, name='monitor_servicetypeadd'),
    url(r'^monitor/servicetypedel', monitor.servicetypedel, name='monitor_servicetypedel'),
    url(r'^monitor/servicetypeedit/(?P<ids>\d+)/$', monitor.servicetypeedit, name='monitor_servicetypeedit'),
    url(r'^monitor/grouplist', monitor.grouplist, name='monitor_grouplist'),
    url(r'^monitor/groupadd', monitor.groupadd, name='monitor_groupadd'),
    url(r'^monitor/groupdel', monitor.groupdel, name='monitor_groupdel'),
    url(r'^monitor/groupedit/(?P<ids>\d+)/$', monitor.groupedit, name='monitor_groupedit'),
    url(r'^monitor/tokenlist', monitor.tokenlist, name='monitor_tokenlist'),
    url(r'^monitor/tokenadd', monitor.tokenadd, name='monitor_tokenadd'),
    url(r'^monitor/tokendel', monitor.tokendel, name='monitor_tokendel'),
    url(r'^monitor/alarmlistedit/(?P<ids>\d+)/$', monitor.alarmlistedit, name='monitor_alarmlistedit'),
    url(r'^monitor/alarmapirecord', monitor.alarmapirecord, name='monitor_alarmapirecord'),
    url(r'^monitor/alarmlogrecord', monitor.alarmlogrecord, name='monitor_alarmlogrecord'),
    url(r'^monitor/alarmapidetail/(?P<ids>\d+)/$', monitor.alarmapidetail, name='monitor_alarmapidetail'),
    url(r'^monitor/alarmlogdetail/(?P<ids>\d+)/$', monitor.alarmlogdetail, name='monitor_alarmlogdetail'),
    url(r'^monitor/ddlogdetail/(?P<ids>\d+)/$', monitor.ddlogdetail, name='monitor_ddlogdetail'),
    url(r'^monitor/setuplist', monitor.setuplist, name='monitor_setuplist'),
    url(r'^monitor/zabbixalart', monitor.zabbixalart, name='monitor_zabbixalart'),
    url(r'^monitor/api/(?P<method>\w+)', monitor.api, name='monitor_api'),
]
