# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory
from virtenviro.content.models import *


class PagesAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ['last_modified']
        
    def clean_parent(self):
        parent = self.cleaned_data.get('parent')
        
        if parent:
            parent = 0
            
        return parent


class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content

        exclude = ['last_modified']

ContentAdminFormset = inlineformset_factory(Page, Content, exclude = ['last_modified'])