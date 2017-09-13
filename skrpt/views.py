from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from skaccounts.permission import permission_verify
from django.core.urlresolvers import reverse
from .models import Rpt
from forms import Rpt_form
@login_required()
@permission_verify()
def index(request):
    temp_name = "skrpt/navi-header.html"
    test01 = Rpt.objects.all()
    return render_to_response("skrpt/index.html", locals(), RequestContext(request))


# Create your views here.
