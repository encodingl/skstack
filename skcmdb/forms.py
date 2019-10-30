#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from .models import Host, Idc, HostGroup, Env, YwGroup, MiddleType, App, DbSource, Url, WhileIp
import sys
import importlib

importlib.reload(sys)



class AssetForm(forms.ModelForm):
    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'other_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'sa': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'env': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'ywgroup': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'middletype': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_no': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'status': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'position': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '物理机写位置，虚机写宿主'}),
            'memo': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;'}),
        }


class IdcForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(IdcForm, self).clean()
        value = cleaned_data.get('name')
        try:
            Idc.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except Idc.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Idc
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'contact': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'contact_phone': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'ip_range': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'jigui': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'bandwidth': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class EnvForm(forms.ModelForm):
    class Meta:
        model = Env
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'address': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'descrition': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class YwGroupForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(YwGroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            YwGroup.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except YwGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = YwGroup
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'sa': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'descrition': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class MiddleTypeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(MiddleTypeForm, self).clean()
        value = cleaned_data.get('name')
        try:
            MiddleType.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except MiddleType.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = MiddleType
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'descrition': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class HostGroupForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(HostGroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            HostGroup.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except HostGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = HostGroup
        exclude = ("id",)


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': '必填项'}),
            'ywgroup': Select(attrs={'class': 'form-control'}),
            'sa': Select(attrs={'class': 'form-control'}),
            'env': Select(attrs={'class': 'form-control'}),
            'belong_ip': SelectMultiple(attrs={'class': 'form-control'}),
            'kafka': SelectMultiple(attrs={'class': 'form-control'}),
            'web_port': TextInput(attrs={'class': 'form-control'}),
            'dubbo_port': TextInput(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'descrition': TextInput(attrs={'class': 'form-control'}),
        }


class UrlForm(forms.ModelForm):
    class Meta:
        model = Url
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': '必填项'}),
            'nickname': TextInput(attrs={'class': 'form-control'}),
            'whitelist': SelectMultiple(attrs={'class': 'form-control'}),
            'mapip': TextInput(attrs={'class': 'form-control'}),
            'ywgroup': Select(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),
            'sa': Select(attrs={'class': 'form-control'}),
            'env': Select(attrs={'class': 'form-control'}),
            'belongapp': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'descrition': Textarea(attrs={'class': 'form-control'}),
        }


class WhileIpForm(forms.ModelForm):
    class Meta:
        model = WhileIp
        exclude = ("id",)
        widgets = {
            'ip': TextInput(attrs={'class': 'form-control', 'placeholder': '必填项'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'descrition': Textarea(attrs={'class': 'form-control', 'style': 'height:150px'}),
        }


class DbSourceForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(DbSourceForm, self).clean()
        value = cleaned_data.get('name')
        try:
            HostGroup.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except HostGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = DbSource
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '主机名称'}),
            'host': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '主机ip'}),
            'user': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '用户名'}),
            'password': PasswordInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '密码'}),
            'port': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '默认3306'}),
            'db': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '数据库名'}),
        }
