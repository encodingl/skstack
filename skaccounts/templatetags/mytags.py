# coding: utf-8


from django import template
import ast

register = template.Library()

@register.filter(name='get_ip')
def get_ip(get_ip):
    return get_ip.nickname