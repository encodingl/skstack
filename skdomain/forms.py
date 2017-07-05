#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import navi, WhiteList

class WhiteList_form(forms.ModelForm):
    class Meta:
        model = WhiteList
        exclude=("id",)

        
        
class navi_form(forms.ModelForm):

#     def clean(self):
#         cleaned_data = super(navi_form, self).clean()
#         value = cleaned_data.get('name')
#         try:
#             navi.objects.get(name=value)
#             self._errors['name']=self.error_class(["%s的信息已经存在" % value])
#         except navi.DoesNotExist:
#             pass
#         return cleaned_data

    class Meta:
        model = navi
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'online_status': forms.Select(attrs={'class': 'form-control'}),            
            'white_list': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
        }

#     def __init__(self,*args,**kwargs):
#         super(RoleListForm,self).__init__(*args,**kwargs)
#         self.fields['name'].label = u'名 称'
#         self.fields['name'].error_messages = {'required':u'请输入名称'}
#         self.fields['permission'].label = u'URL'
#         self.fields['permission'].required = False
        


