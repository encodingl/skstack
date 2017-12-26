#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import history
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from forms import history_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
from django.core.urlresolvers import reverse
from skcmdb.api import get_object
from django.forms.models import model_to_dict  
import re


@login_required()
@permission_verify()
def index(request, *args, **kwargs):
    temp_name = "sktask/setup-header.html"
    allhistory = history.objects.all()
#     allhistory = model_to_dict(allhistory) 
    print allhistory
    return render_to_response("sktask/history.html", locals(), RequestContext(request))

@login_required
@permission_verify_ids()
def detail(request, ids):  
    obj = get_object(history, id=ids)
    obj_cmd = obj.cmd
    ret=obj.cmd_detail
    ret=ret.encode('utf-8')
    return render_to_response('sktask/history_detail.html', locals(), RequestContext(request))