#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from skfile.models import Dirmanager
from django.forms import fields
from django.forms.widgets import *

class dirform(forms.ModelForm):
    widgets = {
        'dirname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),}
    class Meta:
        model=Dirmanager
        exclude = ("id",)
