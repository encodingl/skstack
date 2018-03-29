# coding:utf-8
from django import forms
from django.forms.widgets import *
from models import AlarmGroup, AlarmList, TokenAuth, AlarmRecord, ZabbixRecord, LevelPolicy, ApiRecord
from lib.type import WeiXin_Type, Alarm_TYPE


class LevelPolicyForm(forms.ModelForm):
    class Meta:
        model = LevelPolicy
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'info_policy': SelectMultiple(choices=Alarm_TYPE, attrs={'class': 'form-control'}),
            'warn_policy': SelectMultiple(choices=Alarm_TYPE, attrs={'class': 'form-control'}),
            'error_policy': SelectMultiple(choices=Alarm_TYPE, attrs={'class': 'form-control'}),
            'fatal_policy': SelectMultiple(choices=Alarm_TYPE, attrs={'class': 'form-control'}),
        }


class AlarmGroupForm(forms.ModelForm):
    class Meta:
        model = AlarmGroup
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'serial': Select(choices=WeiXin_Type, attrs={'class': 'form-control'}),
            'user': SelectMultiple(attrs={'class': 'form-control'}),
            'servicetype': Select(attrs={'class': 'form-control'}),
            'levelpolicy': Select(attrs={'class': 'form-control'}),
            'tokens': SelectMultiple(attrs={'class': 'form-control'}),
            'descrition': Textarea(attrs={'class': 'form-control'}),
        }


class AlarmListForm(forms.ModelForm):
    class Meta:
        model = AlarmList
        exclude = ("id", "group")

        widgets = {
            'user': TextInput(attrs={'class': 'form-control', 'style': 'width:500px;', 'readonly': True}),
            'weixin_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                    attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'email_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                   attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'sms_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                 attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'dd_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'tel_status': Select(choices=((True, u'启用'), (False, u'禁用')),
                                 attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'app': SelectMultiple(attrs={'class': 'form-control'}),
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


class AlarmRecordForm(forms.ModelForm):
    class Meta:
        model = AlarmRecord
        exclude = ('id', 'name', 'token', 'type', 'serial', 'level')

        widgets = {
            'create_time': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'receiver': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'type': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'subject': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'content': Textarea(attrs={'class': 'form-control', 'readonly': True}),
        }


class ZabbixRecordForm(forms.ModelForm):
    class Meta:
        model = ZabbixRecord
        exclude = ('id', 'token')

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'create_time': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'appname': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'subject': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'status': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'host': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'event': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'content': Textarea(attrs={'class': 'form-control', 'readonly': True}),
        }


class ApiRecordForm(forms.ModelForm):
    class Meta:
        model = ApiRecord
        exclude = ('id',)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'create_time': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'token': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'groupid': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'level': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'policy': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'subject': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'content': Textarea(attrs={'class': 'form-control', 'readonly': True}),
        }
