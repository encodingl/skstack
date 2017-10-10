from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from skaccounts.permission import permission_verify

from models import UserList
from skcmdb.models import HostGroup

@login_required()
@permission_verify()
def index(request):
    temp_name = "skapi/api-header.html"
    obj_info = HostGroup.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def userlist(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def useradd(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def useredit(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def grouplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def groupadd(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def groupedit(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def setuplist(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def setupedit(request):
    temp_name = "skapi/api-header.html"
    obj_info = UserList.objects.all()
    return render_to_response('skapi/index.html', locals(), RequestContext(request))
