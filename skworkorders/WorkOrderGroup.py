#! /usr/bin/env python
# -*- coding: utf-8 -*-



from models import WorkOrderGroup

from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify


from .forms import WorkOrderGroup_form
from django.shortcuts import render_to_response, RequestContext
from skcmdb.api import get_object

import logging
log = logging.getLogger('skworkorders')



@login_required()
@permission_verify()
def WorkOrderGroup_index(request):
    temp_name = "skworkorders/skworkorders-header.html"    
    tpl_all = WorkOrderGroup.objects.all()
    return render_to_response('skworkorders/WorkOrderGroup_index.html', locals(), RequestContext(request))

@login_required()
@permission_verify()
def WorkOrderGroup_add(request):
    temp_name = "skworkorders/skworkorders-header.html"
    if request.method == "POST":
        tpl_WorkOrderGroup_form = WorkOrderGroup_form(request.POST)
        if tpl_WorkOrderGroup_form.is_valid():
            tpl_WorkOrderGroup_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("skworkorders/WorkOrderGroup_add.html", locals(), RequestContext(request))
    else:
        display_control = "none"
        tpl_WorkOrderGroup_form = WorkOrderGroup_form()
        return render_to_response("skworkorders/WorkOrderGroup_add.html", locals(), RequestContext(request))





@login_required()
@permission_verify()
def WorkOrderGroup_del(request):
    temp_name = "skworkorders/skworkorders-header.html"
    WorkOrderGroup_id = request.GET.get('id', '')  
    if WorkOrderGroup_id:
        try:
            WorkOrderGroup.objects.filter(id=WorkOrderGroup_id).delete()
        except Exception, tpl_error_msg:
            log.warning(tpl_error_msg)
        tpl_all = WorkOrderGroup.objects.all()
        return render_to_response("skworkorders/WorkOrderGroup_index.html", locals(), RequestContext(request))
            
    
    
    

    
    


@login_required()
@permission_verify()
def WorkOrderGroup_edit(request, ids):
    status = 0
    obj = get_object(WorkOrderGroup, id=ids)
    
    if request.method == 'POST':
        tpl_WorkOrderGroup_form = WorkOrderGroup_form(request.POST, instance=obj)
        if tpl_WorkOrderGroup_form.is_valid():
            tpl_WorkOrderGroup_form.save()
            status = 1
        else:
            status = 2
    else:
        tpl_WorkOrderGroup_form = WorkOrderGroup_form(instance=obj)      
    return render_to_response("skworkorders/WorkOrderGroup_edit.html", locals(), RequestContext(request))
