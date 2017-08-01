#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import *

 
        
class Environment_form(forms.ModelForm):
    class Meta:
        model = Environment
        exclude = ("id",)
        widgets = {
           
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
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'user_dep': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
            'env': forms.Select(attrs={'class': 'form-control'}),  
            'group': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.RadioSelect(),
            'repo_url': forms.TextInput(attrs={'class': 'form-control'}),  
            'repo_mode': forms.Select(attrs={'class': 'form-control'}),
            'repo_type': forms.Select(attrs={'class': 'form-control'}),
            'release_user': forms.TextInput(attrs={'class': 'form-control'}),  
            'release_to': forms.TextInput(attrs={'class': 'form-control'}),
            'release_library': forms.TextInput(attrs={'class': 'form-control'}),
            'hosts': forms.TextInput(attrs={'class': 'form-control'}), 
            'pre_deploy': forms.Textarea(attrs={'class': 'form-control'}),
            'post_deploy': forms.Textarea(attrs={'class': 'form-control'}),
            'pre_release': forms.Textarea(attrs={'class': 'form-control'}),
            'post_release': forms.Textarea(attrs={'class': 'form-control'}),
            'post_release_delay': forms.TextInput(attrs={'class': 'form-control'}),
            'audit_enable': forms.Select(attrs={'class': 'form-control'}), 
            'audit_flow': forms.Select(attrs={'class': 'form-control'}),
            'keep_version_num': forms.TextInput(attrs={'class': 'form-control'}),
                 
        }

class TaskCommit_form(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ("project","project_id","project_group","env","user_commit","branch","title", "desc","commit_id",)
        
        widgets = {         
            'project': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'project_id': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'project_group': forms.HiddenInput(attrs={'class': 'form-control'}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_commit': forms.HiddenInput(attrs={'class': 'form-control'}),
            'branch': forms.HiddenInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'commit_id': forms.Select(attrs={'class': 'form-control'}),
 
        }    

        
        
class TaskStatus_form(forms.ModelForm):
    class Meta:
        model = TaskStatus
        exclude = ("id",)

        
class TaskStatus_form2(forms.ModelForm):
    class Meta:
        model = TaskStatus
        exclude = ("id",)
        widgets = {
            'user_commit': forms.TextInput(attrs={'class': 'form-control'}),
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

