from django.db import models
from shop.models import *

class ImageManager(models.Manager):
    def get_one_image(self, product, image_type):
        try:
            image = self.get(product = product, image_type = image_type)
        except Image.DoesNotExist:
            image = None
        return image

class ProductManager(models.Manager):
    def no_blank_parent(self, category = None):
        if category:
            production = self.filter( category = category, parent__isnull = True )
        else:
            production = self.filter( parent__isnull = True )
        product = []
        for p in production:
            childs = p.children.all().count()
            if childs > 0:
                product.append(p)
        return product

    def get_product(self, slug):
        try:
            product = self.get(slug = slug)
        except:
            product = None
        return product

    def filter_group(self):
        return self.all().filter(is_group=True)

    def filter_parent_group(self):
        return self.all().filter(is_group=True, parent__isnull=True)

    def get_product_by_id(self, id):
        try:
            product = self.get(id = id)
        except:
            product = None
        return product

    def get_all_childs(self, id):
        return self.filter(parent = id)

class PropertyManager(models.Manager):
    def by_type(self, property_type, product):
        additional_properties = self.filter(property_type = property_type, product = product)

        return additional_properties