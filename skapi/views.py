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
            if result == 'urllist':
                urls = Url.objects.filter(status=1)
                data = [{'text': i.name, 'value': i.name} for i in urls]
            return HttpResponse(json.dumps(data), content_type="application/json")
        except:
            return HttpResponse("args error")
    return HttpResponse("args error")


def zabbix_sender(request):
    log = logging.getLogger('nginx_info')
    zabbbix_server = request.POST.get('zabbbix_server', '10.8.48.211')
    agent_ip = request.POST.get('agent_ip', '')
    data = request.POST.get('data', '')
    if data and agent_ip:
        datas = data.split('\n')
        count = 0
        data_dict = {}
        for data in datas:
            if data:
                _data = data.split(',')
                url = _data[0].split('-')[0]
                pay_loads = {
                    'bytes_in': int(_data[1]),
                    'bytes_out': int(_data[2]),
                    'http_2xx': int(_data[5]),
                    'http_3xx': int(_data[6]),
                    'http_4xx': int(_data[7]),
                    'http_5xx': int(_data[8]),
                    'rt': int(_data[10]),
                }
                if url in data_dict:
                    data_dict[url]['bytes_in'] += pay_loads['bytes_in']
                    data_dict[url]['bytes_out'] += pay_loads['bytes_out']
                    data_dict[url]['http_2xx'] += pay_loads['http_2xx']
                    data_dict[url]['http_3xx'] += pay_loads['http_3xx']
                    data_dict[url]['http_4xx'] += pay_loads['http_4xx']
                    data_dict[url]['http_5xx'] += pay_loads['http_5xx']
                    data_dict[url]['rt'] += pay_loads['rt']
                else:
                    data_dict[url] = pay_loads
        for url in data_dict:
            for key in data_dict[url]:
                cmd = '''/usr/bin/zabbix_sender -s "%s" -z "%s" -k url[%s,%s] -o "%s"''' % (
                agent_ip, zabbbix_server, url, key, data_dict[url][key])
                code, result = commands.getstatusoutput(cmd)
                if code != 0:
                    count += 1
                    msg = 'error:' + url + ',' + key + ',' + str(data_dict[url][key])
                    log.info(msg)
        if count == 0:
            return HttpResponse('ok')
        else:
            return HttpResponse('Error count:' + str(count))
    return HttpResponse('Error')


def get_urllist(request):
    urls = list(Url.objects.filter(status=1).values_list('name'))
    url_d = [url[0] for url in urls]
    return HttpResponse(json.dumps(url_d), content_type="application/json")

