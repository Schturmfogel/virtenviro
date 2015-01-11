# ~*~ coding: utf-8 ~*~
import os
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from managers import *
from virtenviro.utils import set_slug
from filebrowser.fields import FileBrowseField


class Product(MPTTModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    slug = models.CharField(max_length=60, verbose_name=_('Slug'), null=True, blank=True)
    parent = TreeForeignKey('self', verbose_name=_('Parent'), related_name='children', null=True, blank=True)
    articul = models.CharField(max_length=200, verbose_name=_('Articul'), null=True, blank=True)
    is_group = models.BooleanField(default=False, verbose_name=_('Is Group'))
    description = models.TextField(verbose_name=_('Description'), null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name=_('Production Type'))
    discontinued = models.BooleanField(default=False, verbose_name=_('Discontinued'))
    price = models.FloatField(verbose_name=_('Price'), default=0.0)
    ordering = models.IntegerField(default=0, verbose_name=_('Ordering'), blank=True, null=True)
    manufacturer = models.ForeignKey('Manufacturer', verbose_name=_('Manufacturer'), null=True, blank=True)

    tree = TreeManager()
    objects = ProductManager()

    def __unicode__(self):
        return self.name

    def clean(self, *args, **kwargs):
        if not self.slug:
            self.slug = set_slug(Product, self.name, length=60)

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

    class Meta:
        ordering = ['ordering', 'name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    class MPTTMeta:
        order_insertion_by = ['ordering', 'name']


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


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
    category = models.ManyToManyField(Category, null=True, blank=True, through='PropertyTypeCategoryRelation')
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
    max_count = models.IntegerField(default=1, verbose_name=_('Count'),
                                    help_text=_('Maximum number of properties by this property type in category'))

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


class File(models.Model):
    file = FileBrowseField("File", max_length=200, directory="files/", blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'))

    def __unicode__(self):
        return self.file.url


class ImageType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    category = models.ManyToManyField(Category, verbose_name=_('Production Type'), null=True, blank=True,
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
    image = FileBrowseField("Image", max_length=200, directory=settings.IMAGES_PATH, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name=_('Product'))
    image_type = models.ForeignKey(ImageType, verbose_name=_('Image Type'))
    is_main = models.BooleanField(default=False, verbose_name=_('Is Main'))

    def __unicode__(self):
        return '%s [%s%s]' % (self.name, settings.MEDIA_ROOT, self.image)

    class Meta:
        ordering = ['image_type', 'name']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Manufacturer'), unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True, null=True)
    logo = models.ImageField(upload_to=os.path.join(settings.IMAGES_PATH, 'manufacturers'), verbose_name=_('Logo'),
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


# todo: Disount class
# todo: Delivery
# todo: payment modules
# todo: Currency class
# todo: Warehouse
# todo: Add statistics
# todo: Orders