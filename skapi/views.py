# coding: utf-8
import json, commands

from django.http import HttpResponse
from skcmdb.models import App
import logging
from skcmdb.models import Url


def grafana(request):
    return HttpResponse("ok")


def grafana_search(request):
    if request.method == 'OPTIONS':
        return HttpResponse("")

    if request.method == 'POST':
        try:
            print "result=", request.body
            json_data = json.loads(request.body)
            target_dict = json.loads(json_data['target'])
            result = target_dict.get('result', '')
            if result == 'appname':
                applist = App.objects.filter(status=1)
                data = [{'text': i.name, 'value': i.name} for i in applist]
            if result == 'ip':
                method = target_dict.get('method', '')
                app = App.objects.get(name=method)
                iplist = app.belong_ip.all()
                data = [{'text': i.ip, 'value': i.ip} for i in iplist]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            return HttpResponse("args error")
    return HttpResponse("args error")


def zabbix_sender(request):
    zabbbix_server = request.POST.get('zabbbix_server', '10.8.48.211')
    agent_ip = request.POST.get('agent_ip', '')
    data =request.POST.get('data', '')
    if data and agent_ip:
        datas = data.split('\n')
        for data in datas:
            if data :
                _data = data.split(',')
                url=_data[0].split('-')[0]
                pay_loads = {
                    'bytes_in':_data[1],
                    'bytes_out':_data[2],
                    'http_2xx':_data[5],
                    'http_3xx':_data[6],
                    'http_4xx':_data[7],
                    'http_5xx':_data[8],
                    'rt':_data[10]
                }
                for k in pay_loads:
                    cmd = '''/usr/bin/zabbix_sender -s "%s" -z "%s" -k url[%s,%s] -o "%s"''' % (agent_ip, zabbbix_server, url,k, pay_loads[k])
                    code, result = commands.getstatusoutput(cmd)
                    if code != 0:
                        logging.info(pay_loads)
                return HttpResponse('ok')
    return HttpResponse('error')



def get_urllist(request):
    urls = list(Url.objects.filter(status=1).values_list('name'))
    url_d = [url[0] for url in urls]
    return HttpResponse(json.dumps(url_d), content_type="application/json")
