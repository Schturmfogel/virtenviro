# ~*~ coding: utf-8 ~*~
from django import forms
from datetimewidget.widgets import DateTimeWidget
from django.utils.translation import ugettext_lazy as _
from django.forms import formset_factory
from django.forms.models import modelformset_factory, inlineformset_factory
from virtenviro.content.models import *

__author__ = 'Kamo Petrosyan'


class PagesAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PagesAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Page.objects.filter(is_category=True)

    class Meta:
        model = Page
        exclude = ['last_modified']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Title'), 'class': "form-control"}),
            'slug': forms.TextInput(attrs={'placeholder': _('Slug'), 'class': "form-control"}),
            'template': forms.Select(attrs={'class': "form-control"}),
            'parent': forms.Select(attrs={'class': "form-control"}),
            'ordering': forms.NumberInput(attrs={'class': "form-control", 'min': 0}),
            'pub_datetime': DateTimeWidget(attrs={'id': "id_pub_datetime"}, usel10n=True, bootstrap_version=3),
            'last_modified_by': forms.Select(attrs={'disabled': 'disabled', 'class': 'form-control disabled'})
        }

    def clean_parent(self):
        parent = self.cleaned_data.get('parent')

        if parent:
            parent = 0

        return parent


class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content
        widgets = {
            'pub_datetime': forms.TextInput(attrs={'class': 'form-control', 'required': ''}),
        }
        exclude = ['last_modified']


ContentAdminFormset = inlineformset_factory(Page, Content, exclude=['last_modified'])