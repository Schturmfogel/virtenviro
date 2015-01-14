#~*~ coding: utf-8 ~*~
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from virtenviro.content.models import *
from django import forms
from django.conf import settings
    
class TemplateAdmin(admin.ModelAdmin):
    search_fields = ['title', 'filename']


class PageAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageAdminForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['class'] = 'ckeditor'

    class Meta:
        model = Page
        fields = [
            'title',
            'slug',
            'is_home',
            'intro',
            'content',
            'template',
            'parent',
            'seo_title',
            'seo_keywords',
            'seo_description',
            'published',
            'pub_datetime',
            'author',
            'login_required',
        ]

        def clean_author(self):
            if not self.cleaned_data['author']:
                return User()
            return self.cleaned_data['author']


class PageAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    search_fields = ['title', ]

    form = PageAdminForm

    def save_model(self, request, obj, form, change):
        if not obj.author.id:
            obj.author = request.user
        obj.last_modified_by = request.user
        obj.save()

    class Media:
        try:
            if settings.CKEDITOR:
                js = (
                    '/media/js/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                )
                css = {'all': ('/media/css/ckeditor.css',), }
        except AttributeError:
            pass


admin.site.register(Page, PageAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(AdditionalField)
admin.site.register(FieldValue)
admin.site.register(Snippet)
