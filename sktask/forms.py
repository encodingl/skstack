#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import history,project,job,extravars

    
        
class history_form(forms.ModelForm):
    class Meta:
        model = history
        exclude = ("id",)
        widgets = {
            'login_user': forms.TextInput(attrs={'class': 'form-control'}),
            'src_ip': forms.TextInput(attrs={'class': 'form-control'}),
            'cmd_object': forms.TextInput(attrs={'class': 'form-control'}),
            'task_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cmd': forms.TextInput(attrs={'class': 'form-control'}),
            'cmd_result': forms.TextInput(attrs={'class': 'form-control'}), 
            'cmd_detail': forms.TextInput(attrs={'class': 'form-control'}),            
        }

#     def __init__(self,*args,**kwargs):
#         super(RoleListForm,self).__init__(*args,**kwargs)
#         self.fields['name'].label = u'名 称'
#         self.fields['name'].error_messages = {'required':u'请输入名称'}
#         self.fields['permission'].label = u'URL'
#         self.fields['permission'].required = False
        
class Project_form(forms.ModelForm):
    class Meta:
        model = project
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'path': forms.TextInput(attrs={'class': 'form-control'}),
            'online_status': forms.Select(attrs={'class': 'form-control'}),          
        }

class Job_form(forms.ModelForm):
    class Meta:
        model = job
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'playbook': forms.TextInput(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}), 
            'online_status': forms.Select(attrs={'class': 'form-control'}),          
        }

class Extravars_form(forms.ModelForm):
    class Meta:
        model = extravars
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'vars': forms.Textarea(attrs={'class': 'form-control'}),
            'job': forms.Select(attrs={'class': 'form-control'}), 
            'online_status': forms.Select(attrs={'class': 'form-control'}),          
        }