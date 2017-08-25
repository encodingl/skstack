# coding: utf-8
import json

from django.http import HttpResponse
from skapi.models import Applist
from skcmdb.models import App


def grafana(request):
    print "grafana"
    return HttpResponse("ok")


def grafana_search(request):
    if request.method == 'OPTIONS':
        return HttpResponse("")

    if request.method == 'POST':
        json_data = json.loads(request.body)
        target_data = json_data['target']
        method = json.loads(target_data).get('method','')
    if method == 'appname':
        applist = App.objects.filter(status=1)
        data = [{'text': i.name, 'value': i.name} for i in applist]
        return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        return HttpResponse("args error")

