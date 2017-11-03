#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from skyw.models import Devops,Rota,Notice,event,Platform,PlatFormclass
from django.forms import fields
from django.forms.widgets import *


class devopsform(forms.ModelForm):
    class Meta:
        model = Devops
        exclude = ("id",)
        fields = ('name', 'job', 'iphone', 'jobclass','platform_name', 'businessline','secondaryname')
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'job': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'iphone': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'jobclass':  forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'platform_name': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'businessline': forms.SelectMultiple(attrs={'name':'businessline','class': 'form-control', 'style': 'width:500px;'}),
            'secondaryname': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),}

class rotaform(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ('name','iphone','spell','emergency_contact','iphone_rota')
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'iphone': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'spell': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'emergency_contact': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'iphone_rota': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
        }

class noticeform(forms.ModelForm):
    widgets = {
        'notice': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),}
    class Meta:
        model=Notice
        exclude = ("id",)

class platformclassform(forms.ModelForm):
    class Meta:
        model = PlatFormclass
        exclude = ("id",)


class platformform(forms.ModelForm):
    class Meta:
        model = Platform
        exclude = ("id",)
        fields = ('platform_class', 'platform_name', 'platform_url')
        widgets = {
            'platform_class':  forms.SelectMultiple(attrs={'class': 'form-control'}),
            'platform_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'platform_url': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}), }

class eventform(forms.ModelForm):
    class Meta:
        model = event
        exclude = ("id",)
        fields = ('level','responsetime','processingpersonnel','event','participant')
        widgets = {
            'level': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'responsetime': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'processingpersonnel': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            #'event': forms.TextArea(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'event': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'participant': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:500px;'}),

        }

