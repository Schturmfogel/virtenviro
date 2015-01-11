from models import *
from django.template.loader import render_to_string

class Navigation:
    def __init__(self, product=None, production_type_pk=None):
        self.product = product
        if product is None and production_type_pk:
            try:
                self.production_type = Production_type.objects.get(pk=production_type_pk)
            except:
                pass
        else:
            self.production_type = self.product.production_type
    
    def top_level(self):
        return {'get_children': Product.objects.all().filter(production_type=self.production_type, parent__isnull=True, is_group=True)}
        
    def navigation(self, template=None, nav_top_level_class=None, nav_active_product_class=None):
        nav_parents = self.get_parents(parents=[], product=self.product)
        if template is None:
            template='navigation.html'
            
        navigation_code = ''
        parents = self.get_parents(parents=[], product=self.product)
        for nav_parent in nav_parents:
            navigation_code = render_to_string(template,
                {
                    'active_product': self.product,
                    'nav_parents': nav_parents,
                    'nav_parent': nav_parent,
                    'navigation_code': navigation_code,
                    'nav_active_product_class': nav_active_product_class,
                }
            )
        
        navigation_code = render_to_string(template,
                {
                    'nav_parent': self.top_level(),
                    'nav_parents': nav_parents,
                    'nav_top_levels': self.top_level(),
                    'navigation_code': navigation_code,
                    'nav_top_level_class': nav_top_level_class,
                    'nav_active_product_class': nav_active_product_class,
                }
        )
        
        return navigation_code
            
            
    def get_parents(self, parents=[], product=None):
        if product:
            if not product.is_leaf_node():
                parents.append(product)
        else:
            return parents
        
        self.get_parents(parents = parents, product = product.parent)
        
        return parents