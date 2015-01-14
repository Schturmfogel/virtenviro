from django.contrib import admin
from virtenviro.news.models import Post, Category
from django import forms
from django.conf import settings


class PostAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['class'] = 'ckeditor'
        self.fields['intro'].widget = forms.Textarea(attrs={'class': 'ckeditor'})

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'slug',
            'intro',
            'content',
            'until',
            'origin',
            'author',
            'published',
            'created',
            'seo_title',
            'seo_keywords',
            'seo_description',
        ]


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'intro', 'content']
    list_filter = ('created', )
    form = PostAdminForm

    class Media:
        try:
            if settings.CKEDITOR:
                css = {'all': ('/media/css/ckeditor.css',), }
                js = (
                    '/media/js/ckeditor/ckeditor.js',
                    '/static/filebrowser/js/FB_CKEditor.js',
                    '/media/js/ckeditor.js',
                )
        except AttributeError:
            pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category)