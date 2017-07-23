#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import *

 
        
class Environment_form(forms.ModelForm):
    class Meta:
        model = Environment
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_english': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
          
        }

class ProjectGroup_form(forms.ModelForm):
    class Meta:
        model = ProjectGroup
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        
        }
class Project_form(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'name_english': forms.TextInput(attrs={'class': 'form-control'}),
            'source': forms.Select(attrs={'class': 'form-control'}), 
            'user_create_proj': forms.TextInput(attrs={'class': 'form-control'}),
            'user_dep': forms.Select(attrs={'class': 'form-control'}),
            'evn': forms.Select(attrs={'class': 'form-control'}),  
            'group': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'repo_url': forms.Select(attrs={'class': 'form-control'}),  
            'repo_mode': forms.Select(attrs={'class': 'form-control'}),
            'repo_type': forms.TextInput(attrs={'class': 'form-control'}),
            'release_user': forms.TextInput(attrs={'class': 'form-control'}),  
            'release_to': forms.TextInput(attrs={'class': 'form-control'}),
            'release_library': forms.TextInput(attrs={'class': 'form-control'}),
            'hosts': forms.TextInput(attrs={'class': 'form-control'}), 
            'pre_deploy': forms.TextInput(attrs={'class': 'form-control'}),
            'post_deploy': forms.TextInput(attrs={'class': 'form-control'}),
            'pre_release': forms.TextInput(attrs={'class': 'form-control'}),
            'post_release': forms.TextInput(attrs={'class': 'form-control'}),
            'post_release_delay': forms.TextInput(attrs={'class': 'form-control'}),
            'audit_enable': forms.TextInput(attrs={'class': 'form-control'}), 
            'audit_flow': forms.Select(attrs={'class': 'form-control'}),
            'keep_version_num': forms.TextInput(attrs={'class': 'form-control'}),
            'audit_enable': forms.TextInput(attrs={'class': 'form-control'}),          
        }

class TaskStatus_form(forms.ModelForm):
    class Meta:
        model = TaskStatus
        exclude = ("id",)
        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control'}),
            'action': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}), 
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'link_id': forms.TextInput(attrs={'class': 'form-control'}), 
            'ex_link_id': forms.TextInput(attrs={'class': 'form-control'}),
            'commit_id': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'enable_rollback': forms.TextInput(attrs={'class': 'form-control'}), 
            'created_at': forms.TextInput(attrs={'class': 'form-control'}),

        }

