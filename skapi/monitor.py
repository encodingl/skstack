#coding:utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from skaccounts.permission import permission_verify

from models import AlarmUser, AlarmGroup, AlarmList
from skapi.forms import AlarmUserForm, AlarmGroupForm, AlarmListForm
from lib.utils import get_object
from utils import initAlarmList
from skcmdb.models import HostGroup

@login_required()
@permission_verify()
def index(request):
    temp_name = "skapi/api-header.html"
    alarmgroup_info = AlarmGroup.objects.all()
    alarmgroup_name = request.GET.get('alarmgroup', '')
    obj_info = AlarmList.objects.all()

    if alarmgroup_name:
        obj_info = obj_info.filter(group__contains=alarmgroup_name)
    else:
        obj_info = obj_info.filter(group__contains=AlarmGroup.objects.first().name)
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

def alarmlistedit(request,ids):
    obj = AlarmList.objects.get(id=ids)
    status = 0
    if request.method == "POST":
        form = AlarmListForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
            # else:
            #     status = 2
    else:
        form = AlarmListForm(instance=obj)
    return render_to_response("skapi/alarmlistedit.html", locals(), RequestContext(request))

@login_required()
@permission_verify()
def userlist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmUser.objects.all()
    return render_to_response('skapi/userlist.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def useradd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = AlarmUserForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = AlarmUserForm()
    return render_to_response('skapi/useradd.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def userdel(request):
    id = request.GET.get('id', '')
    if id:
        AlarmList.objects.filter(id=id).delete()
    return HttpResponse(u'删除成功')

@login_required()
@permission_verify()
def useredit(request,ids):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmUser.objects.all()
    status = 0
    obj = get_object(AlarmUser, id=ids)
    if request.method == 'POST':
        af = AlarmUserForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AlarmUserForm(instance=obj)
    return render_to_response('skapi/useredit.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def grouplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmGroup.objects.all()
    return render_to_response('skapi/grouplist.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def groupadd(request):
    temp_name = "skapi/api-header.html"
    if request.method == "POST":
        obj_form = AlarmGroupForm(request.POST)
        if obj_form.is_valid():
            obj_form.save()
            group=AlarmGroup.objects.get(name=obj_form.cleaned_data['name'])
            initAlarmList(group)
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
    else:
        display_control = "none"
        obj_form = AlarmGroupForm()
    return render_to_response('skapi/groupadd.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def groupdel(request):
    id = request.GET.get('id', '')
    if id:
        AlarmGroup.objects.filter(id=id).delete()
    return HttpResponse(u'删除成功')


@login_required()
@permission_verify()
def groupedit(request,ids):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmGroup.objects.all()
    status = 0
    obj = get_object(AlarmGroup, id=ids)
    if request.method == 'POST':
        af = AlarmGroupForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            group = AlarmGroup.objects.get(id=ids)
            initAlarmList(group)
            status = 1
        else:
            status = 2
    else:
        af = AlarmGroupForm(instance=obj)
    return render_to_response('skapi/groupedit.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def setuplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmUser.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def setupedit(request):
    temp_name = "skapi/api-header.html"
    obj_info = AlarmUser.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))
