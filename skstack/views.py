#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,redirect
from skaccounts.permission import permission_verify
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect  



def index(request):
    return redirect('/skrpt/')

