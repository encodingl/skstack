# coding: utf-8


from django import template

register = template.Library()


@register.filter(name='displayName')
def displayName(value, arg):
    return apply(eval('value.get_'+arg+'_display'), ())