# coding:utf-8
from django import forms
from django.forms.widgets import *
from models import AlarmUser, AlarmGroup, AlarmList, TokenAuth, UserPolicy, AlarmRecord, ZabbixRecord


class UserPolicyForm(forms.ModelForm):
    class Meta:
        model = UserPolicy
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
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
        }


class AlarmUserForm(forms.ModelForm):
    class Meta:
        model = AlarmUser
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'tel': TextInput(attrs={'class': 'form-control'}),
            'dd': TextInput(attrs={'class': 'form-control'}),
            'app': SelectMultiple(attrs={'class': 'form-control'}),
            'policy': Select(attrs={'class': 'form-control'}),
        }


class AddAlarmUserForm(forms.ModelForm):
    class Meta:
        model = AlarmUser
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:550px;'}),
            'email': TextInput(attrs={'class': 'form-control', 'style': 'width:550px;'}),
            'tel': TextInput(attrs={'class': 'form-control', 'style': 'width:550px;'}),
            'dd': TextInput(attrs={'class': 'form-control', 'style': 'width:550px;'}),
            'policy': Select(attrs={'class': 'form-control', 'style': 'width:550px;'}),
        }


class AlarmGroupForm(forms.ModelForm):
    class Meta:
        model = AlarmGroup
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'serial': TextInput(attrs={'class': 'form-control'}),
            'user': SelectMultiple(attrs={'class': 'form-control'}),
            'descrition': Textarea(attrs={'class': 'form-control'}),
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
            'tel_status': Select(choices=((0, u'禁用'), (1, u'启用-运维通道'), (2, u'启用-周杰通道')),
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