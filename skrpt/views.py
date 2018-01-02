from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from .models import Rpt
from forms import Rpt_form
from skaccounts.models import UserInfo
from skcmdb.models import Host, App
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
    appnum = user = App.objects.all().count()

      
     #-----------------chart start--------------------------
    date_list = []  
    num_list = []   

    endDate = datetime.date.today() 
    startDate = endDate - datetime.timedelta(days=21) 
    datediff = (endDate - startDate).days
    
    startDate = str(startDate)
    endDate = str(endDate)
    startDateArr = startDate.split("-")
    startDateArr = map(int, startDateArr)
    endDateArr = endDate.split("-")
    endDateArr = map(int, endDateArr)
    begin = datetime.date(startDateArr[0], startDateArr[1], startDateArr[2])
    end = datetime.date(endDateArr[0], endDateArr[1], endDateArr[2])


    d = begin
    delta = datetime.timedelta(days=1)

    while d <= end:  
        m = d.strftime("%Y-%m-%d")
        daynum = history.objects.filter(time_task_finished__contains=m).count()
        date_list.append(m)
        num_list.append(daynum)
        d += delta
   #--------------------------chart end---------------------------------------



    return render_to_response("skrpt/index.html", locals(), RequestContext(request))


# Create your views here.
