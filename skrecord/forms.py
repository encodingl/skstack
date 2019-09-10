#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *

from .models import Record,Record_list,Faq,Faq_list,Assessment,Assessment_list,Change,Track,Track_list,Memo


class Record_form(forms.ModelForm):

    class Meta:
        model = Record
        exclude = ("id",)
        widgets = {
            'eventitle': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventstarttime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventendtime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventpeople': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventclass': Select(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventproduct': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventdescribe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'eventdispose': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Record_list_form(forms.ModelForm):

    class Meta:
        model = Record_list
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'describe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Track_form(forms.ModelForm):

    class Meta:
        model = Track
        exclude = ("id",)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'trackclass': Select(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'trackdescribe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'trackdispose': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'status': Select(choices=(('已解决'), ('跟进中'), ('未解决')), attrs={'class': 'form-control', 'style': 'width:500px;'}),
            #'tracktime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'remarks': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Track_list_form(forms.ModelForm):

    class Meta:
        model = Track_list
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'describe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Faq_form(forms.ModelForm):

    # 验证字段
    # def clean(self):
    #     cleaned_data = super(AssetForm, self).clean()
    #     value = cleaned_data.get('hostname')
    #     try:
    #         Host.objects.get(hostname=value)
    #         self._errors['hostname'] = self.error_class(["%s的信息已经存在" % value])
    #     except Host.DoesNotExist:
    #         pass
    #     return cleaned_data

    class Meta:
        model = Faq
        exclude = ("id",)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            #'problemclass': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'problemclass': Select(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'describe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'solution': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
        }

class Faq_list_form(forms.ModelForm):

    class Meta:
        model = Faq_list
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'describe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Assessment_form(forms.ModelForm):

    class Meta:
        model = Assessment
        exclude = ("id",)
        widgets = {
            'assessmentname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            #'assessmentclass': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'assessmentclass': Select(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'assessmentnum': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'assessmentcontent': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'assessmenttime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'recordpersonnel': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'remarks': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Assessment_list_form(forms.ModelForm):

    class Meta:
        model = Assessment_list
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'describe': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Change_form(forms.ModelForm):

    class Meta:
        model = Change
        exclude = ("id",)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'changetime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'operator': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'business': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'content': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'influence': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'rollback': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'recordtime': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),

        }

class Memo_form(forms.ModelForm):

    class Meta:
        model = Memo
        exclude = ("id",)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'content': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'noticetime': DateTimeInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'expirationtime': DateTimeInput(attrs={'type': 'date', 'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
            'mail': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': '必填项'}),
        }
