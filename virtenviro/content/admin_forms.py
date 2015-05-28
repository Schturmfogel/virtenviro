# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django import forms
from virtenviro.pages.models import *


class PagesAdminForm(forms.ModelForm):
    
    class Meta:
        model = Page
        
    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        
        if parent:
            parent = 0
            
        return parent