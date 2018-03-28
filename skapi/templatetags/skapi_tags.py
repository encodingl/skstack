# coding: utf-8


from django import template

from lib.type import Alarm_TYPE

register = template.Library()


@register.filter(name='exec_data')
def exec_data(value):
    result = []
    if value:
        exec ("value=%s" % value)
        for at in Alarm_TYPE:
            if str(at[0]) in value:
                result.append(at[1])
        value = '\n'.join(result)
    return str(value)
