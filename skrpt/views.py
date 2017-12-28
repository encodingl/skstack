from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify,permission_verify_ids
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
def index(request, *args, **kwargs):
    temp_name = "skrpt/navi-header.html"
    usernum = UserInfo.objects.all().count()
    phynum = Host.objects.filter(group_id__in=[1]).count()
    vmnum = Host.objects.filter(group_id__in=[2]).count()
    appnum = user = App.objects.all().count()

       #sktask-total

    date_list = []
    num_list = []
    cc = ""
    dd = ""
    if request.method == "POST":
       a = request.POST['startDate']
       b = request.POST['endDate']
       now  = datetime.datetime.now()
       now_date = str(datetime.date(now.year,now.month,now.day))
       if b > now_date:
           b = now_date
       cc = a
       dd = b
       if cc >= dd:
           nnn = 1
       else:
           nnn = 0
       startDateArr=a.split("-")
       startDateArr=map(int,startDateArr)
       endDateArr=b.split("-")
       endDateArr=map(int,endDateArr)
       begin = datetime.date(startDateArr[0], startDateArr[1], startDateArr[2])
       end = datetime.date(endDateArr[0], endDateArr[1], endDateArr[2])
       d = begin
       delta = datetime.timedelta(days=1)
       if b > a:
           while d <= end:
             m = d.strftime("%Y-%m-%d")
             daynum = history.objects.filter(time_task_finished__contains=m).count()
             print("a>b:",daynum)
             date_list.append(m)
             num_list.append(daynum)
             d += delta

       else:
           b = datetime.date.today()
           a = b - datetime.timedelta(days=21)
           datediff = (b - a).days
           print(datediff)
           a = str(a)
           b = str(b)
           startDateArr = a.split("-")
           startDateArr = map(int, startDateArr)
           endDateArr = b.split("-")
           endDateArr = map(int, endDateArr)
           begin = datetime.date(startDateArr[0], startDateArr[1], startDateArr[2])
           end = datetime.date(endDateArr[0], endDateArr[1], endDateArr[2])
           d = begin
           delta = datetime.timedelta(days=1)
           while d <= end:
               m = d.strftime("%Y-%m-%d")
               daynum = history.objects.filter(time_task_finished__contains=m).count()
               print("a<b:",daynum)
               date_list.append(m)
               num_list.append(daynum)
               d += delta
    else:
        b = datetime.date.today()
        a = b - datetime.timedelta(days=21)
        datediff = (b - a).days
        a = str(a)
        b = str(b)
        startDateArr = a.split("-")
        startDateArr = map(int, startDateArr)
        endDateArr = b.split("-")
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


    return render_to_response("skrpt/index.html", locals(), RequestContext(request))


# Create your views here.
