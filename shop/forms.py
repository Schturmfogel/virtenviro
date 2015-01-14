#~*~ coding: utf-8 ~*~
from django import forms
from virtenviro.shop.models import *


class XmlImportForm(forms.Form):
    xml_file = forms.FileField()
    parsed_from = forms.CharField(required=False)
    images_path = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    parent = forms.ModelChoiceField(queryset=Product.objects.filter(is_group=True))
    image_type = forms.ModelChoiceField(queryset=ImageType.objects.all())