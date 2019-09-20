from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.urls import reverse
from .models import Rpt
from .forms import Rpt_form
from skaccounts.models import UserInfo
from skcmdb.models import Host, App
from skworkorders.models import WorkOrder,WorkOrderFlow
from sktask.models import history
import  datetime
import time
from django.db.models import Q


@login_required()
@permission_verify()
def index(request):
    temp_name = "skrpt/navi-header.html"
    usernum = UserInfo.objects.all().count()
    phynum = Host.objects.filter(group_id__in=[1]).count()
    vmnum = Host.objects.filter(group_id__in=[2]).count()
    appnum =  App.objects.all().count()
    worklistnum = WorkOrder.objects.filter(status="yes").count()

    print(worklistnum)
     #-----------------chart start--------------------------
    date_list = []  
    num_list_prod = []
    num_list_stg = []

    endDate = datetime.date.today() 
    startDate = endDate - datetime.timedelta(days=14)
    datediff = (endDate - startDate).days
    
    startDate = str(startDate)
    endDate = str(endDate)
    startDateArr = startDate.split("-")
    startDateArr = list(map(int, startDateArr))
    endDateArr = endDate.split("-")
    endDateArr = list(map(int, endDateArr))
    begin = datetime.date(startDateArr[0], startDateArr[1], startDateArr[2])
    end = datetime.date(endDateArr[0], endDateArr[1], endDateArr[2])


    d = begin
    delta = datetime.timedelta(days=1)

    while d <= end:  
        m = d.strftime("%Y-%m-%d")
        # daynum = history.objects.filter(time_task_finished__contains=m).count()
        daynumprod = WorkOrderFlow.objects.filter(finished_at__contains=m, env='prod').count()
        daynumstg = WorkOrderFlow.objects.filter(finished_at__contains=m, env='stg').count()
        date_list.append(m)
        num_list_prod.append(daynumprod)
        num_list_stg.append(daynumstg)
        d += delta
    # print(num_list_prod)
    # print(num_list_stg)
   #--------------------------chart end---------------------------------------



    return render(request,"skrpt/index.html", locals())
 


# Create your views here.
