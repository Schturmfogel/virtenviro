from django import template
from virtenviro.content.models import Snippet, Page, AdditionalField
from django.template import loader, Context
from virtenviro.utils import *

register = template.Library()


@register.assignment_tag
def additional_field(page, field_name):
    try:
        additional_field = AdditionalField.objects.get(name=field_name)
        field = page.fieldvalue_set.filter(additional_field=additional_field)
        if field.count() > 0:
            return field[0]
    except AdditionalField.DoesNotExist:
        return None


@register.simple_tag(takes_context=True)
def render_snippet(context, snippet_name):
    try:
        snippet = Snippet.objects.get(name=snippet_name)
    except Snippet.DoesNotExist:
        snippet = None
    if snippet.render:
        t = loader.get_template_from_string(snippet.code)
        res = t.render(Context(context))
        return res

    return snippet.code


@register.simple_tag(takes_context=True)
def render_content(context, content):
    t = loader.get_template_from_string(content)
    return t.render(Context(context))


@register.simple_tag(takes_context=True)
def render_field(context, page, field_name):
    try:
        additional_field = AdditionalField.objects.get(name=field_name)
    except AdditionalField.DoesNotExist:
        return ''
    field = page.fieldvalue_set.filter(additional_field=additional_field)
    if additional_field.render:
        t = loader.get_template_from_string(field.value)
        return t.render(Context(context))
    else:
        return field.value


@register.assignment_tag(takes_context=True)
def get_pages(context, *args, **kwargs):
    parent_id = kwargs['parent']
    if parent_id == 0:
        queryset = Page.objects.filter(parent__isnull=True)
    else:
        try:
            parent_node = Page.objects.get(id=parent_id)
        except Page.DoesNotExist:
            return None
        level = kwargs.get('level', 1) + 1

        queryset = Page.objects.filter(
            level__lte=level,
            tree_id=parent_node.tree_id,
            lft__gte=parent_node.lft,
            rght__lte=parent_node.rght)
        if not kwargs.get('include_parents', False):
            queryset = queryset.exclude(level__lte=parent_node.level)
        if kwargs.get('author', False):
            queryset = queryset.filter(author=kwargs['author'])
    queryset = queryset.order_by(kwargs.get('order', 'id'))
    if context['request'].GET.has_key('page'):
        rpage = context['request'].GET['page']
    else:
        rpage = 1
    if kwargs.get('limit', False):
        queryset = paginate(queryset, rpage, int(kwargs['limit']))
    return queryset
