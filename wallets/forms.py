from django import forms
from django.forms.widgets import NumberInput

class BVNForm(forms.Form): 
    bvn = forms.CharField(widget=NumberInput(attrs={'class':'form-control', 'placeholder':'Your BVN', 'required':'required'}))