from django import forms
from .models import Rpt

class Rpt_form(forms.ModelForm):
     model = Rpt
     exclude=("id",)
