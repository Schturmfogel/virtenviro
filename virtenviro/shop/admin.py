#~*~ coding: utf-8 ~*~
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.db import models
from django import forms
from models import Product,\
    Category, Property, PropertyType,\
    Image, ImageType, Analog, Manufacturer
    
class APInline(admin.TabularInline):
    model = Property
    extra = 4
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        field = super(APInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        category_id = None
        if request.GET.has_key('category'):
            category_id = request.GET['category']
        else:
            mod = False
            for val in request.path.split('/'):
                try:
                    id = int(val)
                    category_id = Product.objects.get(id = id).category.id
                    mod = True
                    break
                except:
                    pass
        if category_id:
            if db_field.name == 'additional_property_type':
                field.queryset = field.queryset.filter(category = category_id)
        return field
    
class APTInline(admin.TabularInline):
    model = PropertyType.category.through
    extra = 5
    
class ITInline(admin.TabularInline):
    model = ImageType.category.through
    extra = 5


class AnalogInline(admin.TabularInline):
    model = Analog
    extra = 1
    #def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
    #    field = super(AnalogInline, self).formfield_for_foreignkey(db_field, request, **kwargs)   


class ImageInline(admin.TabularInline):
    model = Image
    extra = 5
    def formfield_for_foreignkey(self, db_field, request = None, **kwargs):
        field = super(ImageInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        category_id = None
        if request.GET.has_key('category'):
            category_id = request.GET['category']
        else:
            mod = False
            for val in request.path.split('/'):
                try:
                    id = int(val)
                    category_id = Product.objects.get(id = id).category.id
                    mod = True
                    break
                except:
                    pass
        if category_id and db_field.name == 'image_type':
            field.queryset = field.queryset.filter(category = category_id)
        
        return field


class ProductAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'ckeditor'})

    class Meta:
        model = Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'category__title', 'slug']
    inlines = [
        APInline,
        ImageInline,
        AnalogInline,
    ]

    form = ProductAdminForm
    valid_lookups = ('parent')
    
    list_display = ('name', 'childs_link','is_group', 'add_product_link','discontinued', 'price','ordering')
    list_filter = ('is_group', 'category',)
    list_editable = ('discontinued', 'price', 'ordering')
    def childs_link(self,obj):
        if (obj.is_group):
            return ('<a href="?parent__id__exact=%s">%s</a>' % (obj.id, u'Следующий уровень'))
        else:
            return ''
    childs_link.allow_tags = True
    
    def add_product_link(self, obj):
        return ('<a href="/admin/shop/product/add/?category=%s&parent=%s" class="addlink" onclick="return showAddAnotherPopup(this);">%s</a>' % (obj.category.id, obj.id, u'Добавить продукт'))
    add_product_link.allow_tags = True
    
    def get_form(self, request, obj = None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if request.GET.has_key('category'):
            category_id = request.GET['category']
        elif request.POST.has_key('category'):
            category_id = request.POST['category']
        #elif obj.category.id:
        #    category_id = obj.category.id
        else:
            category_id = None
        if category_id:
            form.base_fields['category'].queryset = form.base_fields['category'].queryset.filter(id = category_id)
            if request.GET.has_key('parent'):
                form.base_fields['parent'].queryset = form.base_fields['parent'].queryset.filter(id = request.GET['parent'])
            else:
                form.base_fields['parent'].queryset = form.base_fields['parent'].queryset.filter(category = category_id, is_group = True)
        return form

    def lookup_allowed(self, lookup, value):
        if lookup.startswith(self.valid_lookups):
            return True
        
        return super(ProductAdmin, self).lookup_allowed(lookup, value)
        
    class Media:
        js = (
            '/media/js/ckeditor/ckeditor.js',
            '/static/filebrowser/js/FB_CKEditor.js',
        )
        css = { 'all': ('/media/css/ckeditor.css',),}
    
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'production_link', 'add_product_link')
    inlines = [APTInline, ITInline]
    
    def add_product_link(self, obj):
        return ('<a href="/admin/shop/product/add/?category=%s" class="addlink">%s</a>' % (obj.id, u'Добавить продукт'))
    add_product_link.allow_tags = True
    
    def production_link(self, obj):
        return ('<a href="/admin/shop/product/?category__id__exact=%s&parent__isnull=True">%s</a>' % (obj.id, u'Продукция'))
    production_link.allow_tags = True

class PropertyTypeAdmin(admin.ModelAdmin):
    search_fields = ['title']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Property)
admin.site.register(PropertyType, PropertyTypeAdmin)
admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(Analog)
admin.site.register(Manufacturer)