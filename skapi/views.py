# coding: utf-8
import json

from django.http import HttpResponse
from skcmdb.models import App


def grafana(request):
    return HttpResponse("ok")


def grafana_search(request):
    if request.method == 'OPTIONS':
        return HttpResponse("")

    if request.method == 'POST':
        try:
            print "result=",request.body
            json_data = json.loads(request.body)
            target_dict = json.loads(json_data['target'])
            result = target_dict.get('result','')
            if result == 'appname':
                applist = App.objects.filter(status=1)
                data = [{'text': i.name, 'value': i.name} for i in applist]
            if result == 'ip':
                method = target_dict.get('method','')
                app = App.objects.get(name=method)
                iplist = app.belong_ip.all()
                data = [{'text': i.ip, 'value': i.id} for i in iplist]
            return HttpResponse(json.dumps(data),content_type="application/json")
        except:
            return HttpResponse("args error")
    return HttpResponse("args error")