# coding:utf-8
from django import forms
from django.forms.widgets import *
from models import AlarmUser, AlarmGroup, AlarmList, TokenAuth


class AlarmUserForm(forms.ModelForm):
    class Meta:
        model = AlarmUser
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;', 'readonly': True}),
            'email': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'dd': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }

class AddAlarmUserForm(forms.ModelForm):
    class Meta:
        model = AlarmUser
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'email': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
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
            'tel_status': Select(choices=( (0, u'禁用'),(1, u'启用-运维'),(2, u'启用-周杰')),
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


class TokenAuthForm(forms.ModelForm):
    class Meta:
        model = TokenAuth
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'token': TextInput(attrs={'class': 'form-control'}),
            'descrition': TextInput(attrs={'class': 'form-control'}),
        }