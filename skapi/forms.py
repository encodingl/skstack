# coding:utf-8
from django import forms
from django.forms.widgets import *
from models import AlarmUser, AlarmGroup, AlarmList


class AlarmUserForm(forms.ModelForm):
    class Meta:
        model = AlarmUser
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'email': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'weixin': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'dd': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class AlarmGroupForm(forms.ModelForm):
    class Meta:
        model = AlarmGroup
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'serial': TextInput(attrs={'class': 'form-control'}),
            'tel_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                          attrs={'class': 'form-control'}),
            'user': SelectMultiple(attrs={'class': 'form-control'}),
            'descrition': TextInput(attrs={'class': 'form-control'}),
        }


class AlarmListForm(forms.ModelForm):
    class Meta:
        model = AlarmList
        exclude = ("id", "group")

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:500px;', 'readonly': True}),
            'weixin_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                    attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'email_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                   attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'sms_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                 attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'dd_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                attrs={'class': 'form-control', 'style': 'width:500px;'}),
        }
