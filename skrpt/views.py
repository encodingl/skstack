from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
# from .models import Rpt
# from .forms import Rpt_form
from skaccounts.models import UserInfo

from skworkorders.models import WorkOrder,WorkOrderFlow

import  datetime

from skaccounts.models import *
from skworkorders.models import *
import time
from django.db.models import Q


@login_required()
@permission_verify()
def index(request):
    temp_name = "skrpt/navi-header.html"
    usernumtotal = UserInfo.objects.filter(is_active=1).count() #激活用户总数
    worklistnum = WorkOrder.objects.filter(status="yes").count() #激活工单总数




    #获取用户组及所属组用户数量
    usergroupall = UserGroup.objects.all().values_list('name','id')
    usergrouplist = [] #存储用户组名称信息
    usergroupnumlist = []#存储所有用户组及用户组的用户数量
    for group in usergroupall:
        usergroupdict = {} #存储单个用户组及用户组的用户数量
        # print(group[0],group[1])
        #group[0]用户组名称，group[1]用户组对应的id
        usergrouplist.append(group[0])
        b = UserGroup.objects.get(id=group[1])
        usernum = b.members.all().count()
        usergroupdict['value'] = usernum
        usergroupdict['name']  = group[0]
        usergroupnumlist.append(usergroupdict)



    # 工单统计
    wonameid = WorkOrderGroup.objects.all().values_list('name','id')
    wonamelist = []
    wonamenumlist = []
    for nameid in wonameid:
        wonamenumdict = {}
        wonamelist.append(nameid[0])
        wonum = WorkOrder.objects.filter(group_id=nameid[1]).count()
        wonamenumdict['value'] = wonum
        wonamenumdict['name'] = nameid[0]
        wonamenumlist.append(wonamenumdict)


    #工单执行数统计
    weekoffset = datetime.datetime.now().weekday()
    datelist = []
    datelisttemp = []
    for i in range(5):
        weekstartday = (datetime.datetime.now() - datetime.timedelta(days=weekoffset))
        print(weekstartday)
        datelist.append(weekstartday.strftime("%Y%m%d"))
        datelisttemp.append(weekstartday.strftime("%Y-%m-%d"))
        weekoffset = weekoffset + 7
    datelist.reverse()
    envname = Environment.objects.all().values('name_english')
    envnamelist = []
    envdictnum = {'type':'line','stack':'总量'}
    envdictnumlist = []
    for ename in envname:
        envdictnum['name'] = ename
        envnamelist.append(ename['name_english'])

    for eename in envnamelist:
        vauledate = []
        envdictnum =  {'type': 'line', 'stack': '总量'}
        for start in datelisttemp:
            envdictnum['name'] = eename
            startdate = datetime.datetime.strptime(start,"%Y-%m-%d").date()
            enddate = startdate + datetime.timedelta(days=6)
            numdate = WorkOrderFlow.objects.filter(finished_at__gte=startdate,finished_at__lte=enddate,env=eename).count()
            vauledate.append(numdate)
        envdictnum['data'] = vauledate
        envdictnumlist.append(envdictnum)
    return render(request,"skrpt/index.html", locals())
 


# Create your views here.
