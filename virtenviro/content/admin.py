#~*~ coding: utf-8 ~*~
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django import forms
from django.conf import settings
from virtenviro.content.models import *


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
            'template',
            'parent',
            'published',
            'pub_datetime',
            'author',
            # 'last_modified_by',
            'login_required'
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['initial'] = request.user.id

        if db_field.name == 'last_modified_by':
            kwargs['initial'] = request.user.id
        return super(PageAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    class Media:
        try:
            if settings.CKEDITOR:
                js = (
                    '/static/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                    '/static/js/ckeditor.js',
                )
                css = {'all': ('/static/css/ckeditor.css',), }
        except AttributeError:
            pass


admin.site.register(Page, PageAdmin)
admin.site.register(Content)
admin.site.register(Template, TemplateAdmin)
admin.site.register(AdditionalField)
admin.site.register(FieldValue)
admin.site.register(Snippet)
