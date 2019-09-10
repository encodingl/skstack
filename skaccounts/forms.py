#! /usr/bin/env python
# -*- coding: utf-8 -*-
# update by guohongze@126.com
from django import forms
from django.contrib import auth
from .models import UserInfo, RoleList, PermissionList, RoleJob, AuditFlow, UserGroup
from lib.type import User_TYPE


class LoginUserForm(forms.Form):
    username = forms.CharField(label='账 号', error_messages={'required': '账号不能为空'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密 码', error_messages={'required': '密码不能为空'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class AddUserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'password', 'nickname', 'email', 'tel', 'dd', 'type', 'role', 'role_job', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': ' form-control'}),
            'tel': forms.TextInput(attrs={'class': ' form-control'}),
            'dd': forms.TextInput(attrs={'class': ' form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(choices=User_TYPE, attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'role': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'role_job': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'is_active': forms.Select(choices=((True, '启用'), (False, '禁用')), attrs={'class': 'form-control', 'style': 'width:500px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '账 号'
        self.fields['username'].error_messages = {'required': '请输入账号'}
        self.fields['password'].label = '密 码'
        self.fields['password'].error_messages = {'required': '请输入密码'}
        self.fields['email'].label = '邮 箱'
        self.fields['email'].error_messages = {'required': '请输入邮箱', 'invalid': '请输入有效邮箱'}
        self.fields['tel'].label = '电 话'
        self.fields['dd'].label = '钉 钉'
        self.fields['nickname'].label = '姓 名'
        self.fields['nickname'].error_messages = {'required': '请输入姓名'}
        self.fields['type'].label = '类 型'
        self.fields['role'].label = '菜单角色'
        self.fields['role_job'].label = 'Ansible任务角色'
        self.fields['is_active'].label = '状 态'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('密码必须大于6位')
        return password


class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'nickname', 'email', 'tel', 'dd', 'type', 'role', 'role_job', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'tel': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'dd': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'type': forms.Select(choices=User_TYPE, attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'role': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'role_job': forms.Select(attrs={'class': 'form-control', 'style': 'width:500px;'}),
            'is_active': forms.Select(choices=((True, '启用'), (False, '禁用')),
                                      attrs={'class': 'form-control', 'style': 'width:500px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '账 号'
        self.fields['username'].error_messages = {'required': '请输入账号'}
        self.fields['email'].label = '邮 箱'
        self.fields['email'].error_messages = {'required': '请输入邮箱', 'invalid': '请输入有效邮箱'}
        self.fields['tel'].label = '电 话'
        self.fields['dd'].label = '钉 钉'
        self.fields['nickname'].label = '姓 名'
        self.fields['nickname'].error_messages = {'required': '请输入姓名'}
        self.fields['type'].label = '类 型'
        self.fields['role'].label = '菜单角色'
        self.fields['role_job'].label = 'Ansible任务角色'
        self.fields['is_active'].label = '状 态'

    def clean_password(self):
        return self.cleaned_data['password']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', error_messages={'required': '请输入原始密码'},
                                   widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:500px;'}))
    new_password1 = forms.CharField(label='新密码', error_messages={'required': '请输入新密码'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'style': 'width:500px;'}))
    new_password2 = forms.CharField(label='新密码', error_messages={'required': '请重复新输入密码'},
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'style': 'width:500px;'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1) < 6:
            raise forms.ValidationError('密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class RoleListForm(forms.ModelForm):
    class Meta:
        model = RoleList
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permission': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoleListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '名 称'
        self.fields['name'].error_messages = {'required': '请输入名称'}
        self.fields['permission'].label = 'URL'
        self.fields['permission'].required = False


class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PermissionListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '名 称'
        self.fields['name'].error_messages = {'required': '请输入名称'}
        self.fields['url'].label = 'URL'
        self.fields['url'].error_messages = {'required': '请输入URL'}


class RoleJobForm(forms.ModelForm):
    class Meta:
        model = RoleJob
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permission': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super(RoleJobForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '名 称'
        self.fields['name'].error_messages = {'required': '请输入名称'}
        self.fields['permission'].label = 'job权限'
        self.fields['permission'].required = False


class AuditFlow_form(forms.ModelForm):
    class Meta:
        model = AuditFlow
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.TextInput(attrs={'class': 'form-control'}),
            'l1': forms.Select(attrs={'class': 'form-control'}),
            'l2': forms.Select(attrs={'class': 'form-control'}),
            'l3': forms.Select(attrs={'class': 'form-control'}),

        }


class UserGroup_form(forms.ModelForm):
    class Meta:
        model = UserGroup
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
        }
