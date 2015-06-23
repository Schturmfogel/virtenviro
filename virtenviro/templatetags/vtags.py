# ~*~ coding: utf-8 ~*~
__author__ = 'Kamo Petrosyan'
from django import template
#from django.template import loader, Context
#from django.db import  models
#from virtenviro.content.models import Snippet, Page, AdditionalField
#from virtenviro.shop.models import *
#from virtenviro.utils import *

register = template.Library()


@register.filter
def base64(value):
    return value.encode('base64', 'strict')


class Base64Node(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return output.encode('utf-8').encode('base64', 'strict').strip().replace('\n', '')


@register.tag
def base64_block(parser, token):
    nodelist = parser.parse(('endbase64_block',))
    parser.delete_first_token()
    return Base64Node(nodelist)