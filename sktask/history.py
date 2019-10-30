#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from .models import history
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from .forms import history_form
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from skcmdb.api import get_object
from django.forms.models import model_to_dict  
import re


@login_required()
@permission_verify()
def index(request):
    temp_name = "sktask/setup-header.html"
    allhistory = history.objects.all()
#     allhistory = model_to_dict(allhistory) 
    print(allhistory)
    return render(request,"sktask/history.html", locals())

@login_required
@permission_verify()
def detail(request, ids):  
    obj = get_object(history, id=ids)
    obj_cmd = obj.cmd
    ret=obj.cmd_detail
    ret=ret.encode('utf-8')
    return render(request,'sktask/history_detail.html', locals())