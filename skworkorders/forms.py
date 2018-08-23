#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Environment,WorkOrder,WorkOrderFlow,WorkOrderGroup,Vars,VarsGroup,ConfigCenter


from django_celery_results.models import TaskResult 

class ConfigCenter_form(forms.ModelForm):
    class Meta:
        model = ConfigCenter
        exclude = ("id",)
        widgets = {
             
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'rsa_key': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
          
class Environment_form(forms.ModelForm):
    class Meta:
        model = Environment
        exclude = ("id",)
        widgets = {
           
            'name_english': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
          
        }

class WorkOrderGroup_form(forms.ModelForm):
    class Meta:
        model = WorkOrderGroup
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
        
        }
class WorkOrder_form(forms.ModelForm):
    class Meta:
        model = WorkOrder
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'user_dep': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
            'env': forms.Select(attrs={'class': 'form-control'}),  
            'group': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.RadioSelect(),
            
            'var_built_in': forms.Textarea(attrs={'class': 'form-control'}),
            'var_opional_switch': forms.CheckboxInput(),
            'var_opional': forms.Select(attrs={'class': 'form-control'}),
            
            
            'pre_task': forms.Textarea(attrs={'class': 'form-control'}),
            'main_task': forms.Textarea(attrs={'class': 'form-control'}),
            'post_task': forms.Textarea(attrs={'class': 'form-control'}),
            
            'audit_enable': forms.CheckboxInput(), 
            'audit_flow': forms.Select(attrs={'class': 'form-control'}),
            
            'schedule_enable': forms.CheckboxInput(), 
#   
            
            'template_enable': forms.CheckboxInput(), 
             'config_center': forms.Select(attrs={'class': 'form-control'}),
    
                 
        }

class WorkOrderCommit_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("title","workorder","workorder_id","workorder_group","env","user_commit","desc","status","audit_level","celery_schedule_time","back_exe_enable","auto_exe_enable")
        
        widgets = {    
            'title': forms.TextInput(attrs={'class': 'form-control','readonly':True}),     
            'workorder': forms.HiddenInput(attrs={'class': 'form-control'}),
            'workorder_id': forms.HiddenInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_group': forms.HiddenInput(attrs={'class': 'form-control'}),
            'env': forms.HiddenInput(attrs={'class': 'form-control'}),
            'user_commit': forms.HiddenInput(attrs={'class': 'form-control'}),
        
            
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            
            'celery_schedule_time': forms.DateTimeInput(attrs={'class': 'form-control'}),
      
            'status': forms.HiddenInput(attrs={'class': 'form-control'}),
            'audit_level': forms.HiddenInput(attrs={'class': 'form-control'}),
            'back_exe_enable': forms.CheckboxInput(), 
            'auto_exe_enable': forms.CheckboxInput(), 
           
      
 
        }    

class WorkOrderCommit_help_form(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ("name","desc")
        
        widgets = {    
            'name': forms.TextInput(attrs={'class': 'form-control','readonly':True}),     
            'desc': forms.Textarea(attrs={'class': 'form-control','readonly':True}),

        }  
 
 
class WorkOrderFlow_release_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("id","workorder","desc","env",'user_vars')
         
        widgets = {         
            'workorder': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'id': forms.HiddenInput(attrs={'class': 'form-control'}),
            'desc': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_vars': forms.Textarea(attrs={'class': 'form-control','style': 'height: 60px;','readonly':True}),
 
  
        }  
                
class WorkOrderFlow_detail_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        exclude = ("id",)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_commit': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_group': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_id': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'status': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'desc': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
            'user_vars': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
            'audit_level': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l1': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'comment_l1': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l1': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l2': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'comment_l2': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l2': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l3': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'comment_l3': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l3': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'finished_at': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'celery_task_id': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'celery_schedule_time': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'finished_at': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'back_exe_enable': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'auto_exe_enable': forms.TextInput(attrs={'class': 'form-control','readonly':True}),

        }    

        
class WorkOrderFlow_schedule_detail_form(forms.ModelForm):
    class Meta:
        model = TaskResult
        exclude = ("id",)
        widgets = {
            'task_id': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'status': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'content_type': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'content_encoding': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'result': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
#             'date_done': forms.DateTimeField(),
            'traceback': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
     
        }  
        
class CeleryTaskResult_form(forms.Form):
    task_id = forms.CharField(label=u'task_id', widget=forms.TextInput(attrs={'class': 'form-control','readonly':True}))
    status = forms.CharField(label=u'status', widget=forms.TextInput(attrs={'class': 'form-control','readonly':True}))
    result = forms.CharField(label=u'result', widget=forms.Textarea(attrs={'class': 'form-control','readonly':True}))
    date_done = forms.CharField(label=u'date_done', widget=forms.TextInput(attrs={'class': 'form-control','readonly':True}))
    traceback = forms.CharField(label=u'traceback', widget=forms.Textarea(attrs={'class': 'form-control','readonly':True}))
    
    
    
 
class WorkOrderFlow_rollback_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("workorder","workorder_id","env","desc")
         
        widgets = {         
            'workorder': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_id': forms.HiddenInput(attrs={'class': 'form-control'}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'desc': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
         
  
        }  
         
class VarsGroup_form(forms.ModelForm):
    class Meta:
        model = VarsGroup
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'vars': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
            'env': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        
        }
        
class Vars_form(forms.ModelForm):
    class Meta:
        model = Vars
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'label_name': forms.TextInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
            'value_method': forms.Select(attrs={'class': 'form-control'}),
            'value_form_type': forms.Select(attrs={'class': 'form-control'}),
            'value_optional': forms.Textarea(attrs={'class': 'form-control'}),
            'vars': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10', 'multiple': 'multiple'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'env': forms.Select(attrs={'class': 'form-control'}),
            'value_script': forms.TextInput(attrs={'class': 'form-control'}),
            
        
        }
        

    
class Custom_form(forms.Form):
    pass

class Comment_form(forms.Form):
    comment_content = forms.CharField(label=u'意见',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
