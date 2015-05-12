# ~*~ coding: utf-8 ~*~
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from filebrowser.fields import FileBrowseField
from django.conf import settings
from virtenviro.shop.managers import *
from virtenviro.utils import set_slug, sha256, id_generator

MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', getattr(settings, 'STATIC_ROOT'))


class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), related_name='subcategories', null=True, blank=True)
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    image = models.ImageField(upload_to=_(os.path.join(MEDIA_ROOT, 'img', 'shop', 'category')), verbose_name=_('Image'), null=True, blank=True)

    # META FIELDS
    meta_title = models.CharField(max_length=250, verbose_name=_('Meta Title'), null=True, blank=True)
    meta_keywords = models.TextField(verbose_name=_('Meta Keywords'), null=True, blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), null=True, blank=True)

    # SERVICE FIELDS
    ordering = models.IntegerField(default=0, verbose_name=_('Ordering'), blank=True, null=True)
    view_count = models.IntegerField(default=0, verbose_name=_('Count of views'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.parent is None:
            return '/%s/' % self.slug
        if self.is_home:
            return '/'
        url = self.get_all_ancestors(self.parent, self.slug)
        return '%s' % url

    get_absolute_url.short_description = _('URL')

    def get_all_ancestors(self, parent, url=''):
        url = '%s/%s' % (parent.slug, url)
        if parent.parent:
            return self.get_all_ancestors(parent.parent, url)
        else:
            return '/%s/' % url

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name=_('Category'), related_name='children', null=True, blank=True)
    subcategory = models.ManyToManyField(Category, verbose_name=_('Subcategory'), related_name='products', blank=True)
    articul = models.CharField(max_length=200, verbose_name=_('Articul'), null=True, blank=True)
    '''
    Так как не удалось при импорте сгенерировать корректные unique_code, и данные могут быть не полные или не совпадать,
    то решено временно или навсегда удалить это поле
    #unique_code = models.CharField(max_length=250, verbose_name=_('Unique code'), unique=True, blank=True)
    '''
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    price = models.FloatField(verbose_name=_('Price'), default=0.0)
    manufacturer = models.ForeignKey('Manufacturer', verbose_name=_('Manufacturer'), null=True, blank=True)

    # META FIELDS
    meta_title = models.CharField(max_length=250, verbose_name=_('Meta Title'), null=True, blank=True)
    meta_keywords = models.TextField(verbose_name=_('Meta Keywords'), null=True, blank=True)
    meta_description = models.TextField(verbose_name=_('Meta Description'), null=True, blank=True)

    # SERVICE FIELDS
    ordering = models.IntegerField(default=0, verbose_name=_('Ordering'), blank=True, null=True)
    view_count = models.IntegerField(default=0, verbose_name=_('Count of views'), blank=True, null=True)

    objects = ProductManager()

    def __unicode__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if not self.slug:
            self.slug = set_slug(Product, self.name, length=60)

        if not self.articul:
            self.articul = id_generator(size=15)
        '''
        if not self.unique_code:
            if self.manufacturer:
                manufacturer = self.manufacturer.name
            else:
                manufacturer = ''
            unique_code_string = '{}{}{}'.format(self.name, manufacturer, self.articul)
            self.unique_code = sha256(unique_code_string)
        '''

    def get_main_images(self):
        return self.image_set.all().filter(is_main=True)

    def get_main_image(self):
        main_images = self.image_set.all().filter(is_main=True)
        if not main_images:
            return None
        else:
            return main_images[0]

    def has_main_image(self):
        if self.image_set.all().filter(is_main=True):
            return True
        else:
            return False
        return False

    def filter_group(self):
        return self.filter(is_group=True)

    def filter_parent_group(self):
        return self.filter(is_group=True, parent__isnull=True)

    def get_absolute_url(self):
        return '%s%s' % (self.category.get_absolute_url(), self.slug)

    get_absolute_url.short_description = _('URL')

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class MPTTMeta:
        order_insertion_by = ['ordering', 'name']


class PropertyType(models.Model):
    DATA_TYPES = (
        (-1, _('Integer'),),
        (-2, _('Float')),
        (-3, _('String')),
        (-4, _('Text')),
        (-5, _('Boolean')),
        (-6, _('Html')),
    )
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ManyToManyField(Category, through='PropertyTypeCategoryRelation')
    data_type = models.IntegerField(verbose_name=_('Data type'), default=-1, choices=DATA_TYPES)

    def __unicode__(self):
        return '%s [%s]' % (self.name, self.pk)

    class Meta:
        ordering = ['name']
        verbose_name = _('Properties type')
        verbose_name_plural = _('Properties Types')


class PropertyTypeCategoryRelation(models.Model):
    property_type = models.ForeignKey(PropertyType, verbose_name=_('Property Type'))
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    # Set maximum number of Property types for category to economy space
    max_count = models.IntegerField(
        default=1,
        verbose_name=_('Count'),
        help_text=_('Maximum number of properties by this property type in category'))
    # slug to create groups of filters as pages
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)

    def __unicode__(self):
        return '%s for %s' % (self.property_type.name, self.category.name)


class Property(models.Model):
    property_type = models.ForeignKey(PropertyType)
    value = models.TextField(verbose_name=_('Value'))
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    objects = PropertyManager()

    def __unicode__(self):
        return '%s: %s' % (self.property_type.name, self.value)

    class Meta:
        ordering = ['property_type__name', 'value']
        verbose_name = _('Property')
        verbose_name_plural = _('Properties')


class PropertySlug(models.Model):
    """
    This class created to make available create pages categories of goods with filtration by
    property type and property value.
    For example:
        You have shorts.
        You can group them by property_type "Color". There will be all properties by "color", grouped by "value"
        You can then get all shorts with color "Red"
    """
    property_type = models.ForeignKey(PropertyType)
    value = models.TextField(verbose_name=_('Value'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'))

    def __unicode__(self):
        return '%s: %s' % (self.property_type.name, self.value)

    class Meta:
        ordering = ['value']
        verbose_name = _('Property slug')
        verbose_name_plural = _('Property slugs')


class File(models.Model):
    file = FileBrowseField("File", max_length=200, directory="files/", blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    def __unicode__(self):
        return self.file.url


class ImageType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ManyToManyField(Category, verbose_name=_('Production Type'),
                                      through='ImageTypeCategoryRelation')
    '''
    def clean(self):
        from django.core.exceptions import ValidationError
        self.images_path = '%s' % self.images_path
    '''

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Images Type')
        verbose_name_plural = _('Images Types')


class ImageTypeCategoryRelation(models.Model):
    image_type = models.ForeignKey(ImageType, verbose_name=_('Image type'))
    category = models.ForeignKey(Category, verbose_name=_('Category'))
    max_count = models.IntegerField(default=1, verbose_name=_('Count'),
                                    help_text=_('Maximum number of images by this image type in category'))

    def __unicode__(self):
        return '%s for %s' % (self.image_type.name, self.category.name)


class Image(models.Model):
    image = FileBrowseField("Image", max_length=200, directory=os.path.join(MEDIA_ROOT, 'img', 'shop'),
                            blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    image_type = models.ForeignKey(ImageType, verbose_name=_('Image Type'))
    is_main = models.BooleanField(default=False, verbose_name=_('Is Main'))

    def __unicode__(self):
        return '%s [%s%s]' % (self.name, MEDIA_ROOT, self.image)

    class Meta:
        ordering = ['image_type', 'name']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Manufacturer'), unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    logo = models.ImageField(upload_to=os.path.join(MEDIA_ROOT, 'img', 'shop', 'manufacturers'), verbose_name=_('Logo'),
                             null=True, blank=True)

    # Contacts
    country = models.CharField(max_length=150, verbose_name=_('Country'), blank=True, null=True)
    city = models.CharField(max_length=150, verbose_name=_('City'), blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name=_('Address'), blank=True, null=True)
    phones = models.TextField(verbose_name=_('Phones'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Manufacturer')
        verbose_name_plural = _('Manufacturers')


# todo: Discount class
# todo: Delivery
# todo: payment modules
# todo: Currency class
class Currency(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Currency'))
    default = models.BooleanField(default=False, verbose_name=_('Is default currency'))
    symbol = models.CharField(max_length=10, verbose_name=_('Symbol'), blank=True, null=True)
    char_code = models.CharField(max_length=10, verbose_name=_('Char code of currency'), blank=True, null=True)
    num_code = models.IntegerField(verbose_name=_('Code of currency'), blank=True, null=True)
    nominal = models.FloatField(verbose_name=_('Nominal'), blank=True, null=True)
    value = models.FloatField(verbose_name=_('Value'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

# todo: Warehouse
# todo: Add statistics
# todo: Orders
