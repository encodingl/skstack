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
            
            'pre_task': forms.Textarea(attrs={'class': 'form-control'}),
            'main_task': forms.Textarea(attrs={'class': 'form-control'}),
            'post_task': forms.Textarea(attrs={'class': 'form-control'}),
            
            'audit_enable': forms.CheckboxInput(), 
            'audit_flow': forms.Select(attrs={'class': 'form-control'}),
            'template_enable': forms.CheckboxInput(), 
    
                 
        }

class WorkOrderCommit_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("title","workorder","workorder_id","workorder_group","env","user_commit","desc","status","audit_level")
        
        widgets = {    
            'title': forms.TextInput(attrs={'class': 'form-control','readonly':True}),     
            'workorder': forms.HiddenInput(attrs={'class': 'form-control'}),
            'workorder_id': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_group': forms.HiddenInput(attrs={'class': 'form-control'}),
            'env': forms.HiddenInput(attrs={'class': 'form-control'}),
            'user_commit': forms.HiddenInput(attrs={'class': 'form-control'}),
        
            
            'desc': forms.Textarea(attrs={'class': 'form-control'}),
      
            'status': forms.HiddenInput(attrs={'class': 'form-control'}),
            'audit_level': forms.HiddenInput(attrs={'class': 'form-control'}),
           
      
 
        }    


 
 
class WorkOrderFlow_release_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("workorder","workorder_id","env")
         
        widgets = {         
            'workorder': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'workorder_id': forms.HiddenInput(attrs={'class': 'form-control'}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
 
  
        }  
                
class WorkOrderFlow_detail_form(forms.ModelForm):
    class Meta:
        model = WorkOrderFlow
        fields = ("workorder","env","desc","audit_level","user_l1","updated_at_l1","user_l2","updated_at_l2","user_l3","updated_at_l3","finished_at",)
        widgets = {
            'workorder': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'env': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'desc': forms.Textarea(attrs={'class': 'form-control','readonly':True}),
            
            'audit_level': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l1': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l1': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l2': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l2': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'user_l3': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'updated_at_l3': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            'finished_at': forms.TextInput(attrs={'class': 'form-control','readonly':True}),
            
  
        }    
 
 
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
            'evn': forms.Select(attrs={'class': 'form-control'}),
        
        }
        
class Vars_Select_form(forms.Form):
    value_optional = forms.ChoiceField(label=u'变量名', error_messages={'required': u'不能为空'},
                               widget=forms.Select(attrs={'class': 'form-control'}))
