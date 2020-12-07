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
    execworkenum = WorkOrderFlow.objects.filter().count()        #提交工单总数
    envnum = Environment.objects.filter().count()                #工单环境总数

    #工单执行分类统计
    execstatusnumlist = []#工单执行分类统计列表
    execstatuslist = ['待审核','审核拒绝','待执行','执行成功','执行失败','已撤销'] #统计执行工单状态分类列表
    #待审核
    onsnum = WorkOrderFlow.objects.filter(audit_level=1,status=0) .count() #审核层级为1级
    secnum = WorkOrderFlow.objects.filter(audit_level=2,status__in=[0,1]) .count()#审核层级为2级
    threenum = WorkOrderFlow.objects.filter(audit_level=3,status__in=[0,1,5]).count() #审核层级为3级
    auditallnum = onsnum + secnum + threenum
    auditdict = {'value':auditallnum,'name':'待审核'}

    #审核拒绝
    refusenum = WorkOrderFlow.objects.filter(status__in=[2,6,8]).count()
    refusedict = {'value':refusenum,'name':'审核拒绝'}

    #待执行
    onsnum = WorkOrderFlow.objects.filter(audit_level=1, status=1).count()  # 审核层级为1级
    secnum = WorkOrderFlow.objects.filter(audit_level=2, status=5).count()  # 审核层级为2级
    threenum = WorkOrderFlow.objects.filter(audit_level=3, status=7).count()#审核层级为3级
    pendallnum = onsnum + secnum + threenum
    penddict = {'value': pendallnum, 'name':'待执行'}
    #执行成功
    sucnum = WorkOrderFlow.objects.filter(status=3).count()
    sucdict = {'value': sucnum, 'name': '执行成功'}
    #执行失败
    failnum = WorkOrderFlow.objects.filter(status=4).count()
    faildict = {'value': failnum, 'name': '执行失败'}
    #已撤销
    revokenum = WorkOrderFlow.objects.filter(status=9).count()
    revokedict = {'value': revokenum, 'name': '已撤销'}
    execstatusnumlist.extend([auditdict,refusedict,penddict,sucdict,faildict,revokedict])




    #环境工单分类统计
    envnameid = Environment.objects.all().values_list('name_english', 'id')
    envlist = []  # 环境名
    envnumlist = []  # 存储所有环境名及环境对应的激活工单总数
    for group in envnameid:
        envnum_dict = {}   #单个环境及激活工单数
        envlist.append(group[0])
        numnum = WorkOrder.objects.filter(env_id=group[1],status='yes').count()
        envnum_dict['value']=numnum
        envnum_dict['name']  = group[0]
        envnumlist.append(envnum_dict)








    #获取用户组及所属组用户数量
    usergroupall = UserGroup.objects.all().values_list('name','id')
    usergrouplist = [] #存储用户组名称信息
    usergroupnumlist = []#存储所有用户组及用户组的用户数量
    for group in usergroupall:
        usergroupdict = {} #存储单个用户组及用户组的用户数量
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
    weekoffset = datetime.datetime.now().weekday() + 2
    datelist = []
    datelisttemp = []
    for i in range(5):
        weekstartday = (datetime.datetime.now() - datetime.timedelta(days=weekoffset))
        weekendday = weekstartday + datetime.timedelta(days=6)
        datelist.append(weekendday.strftime("%Y%m%d"))
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
        envdictnum =  {'type': 'line'}
        for start in datelisttemp:
            envdictnum['name'] = eename
            startdate = datetime.datetime.strptime(start,"%Y-%m-%d").date()
            enddate = startdate + datetime.timedelta(days=6)

            numdate = WorkOrderFlow.objects.filter(finished_at__gte=startdate,finished_at__lte=enddate,env=eename).count()
            vauledate.append(numdate)
        vauledate.reverse()
        envdictnum['data'] = vauledate
        envdictnumlist.append(envdictnum)
    return render(request,"skrpt/index.html", locals())
 


# Create your views here.
