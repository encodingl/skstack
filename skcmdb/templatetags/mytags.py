# coding: utf-8


from django import template
import ast

register = template.Library()


@register.filter(name='int2str')
def int2str(value):
    """
    int 转换为 str
    """
    return str(value)


@register.filter(name='res_splict')
def res_splict(value):
    """
    将结果格式化换行
    """
    res = []
    if isinstance(value, tuple):
        for v in value:
            if v is not None:
                data = v.replace('\n', '<br>')
                res.append(data)
        return res
    elif isinstance(value, basestring): 
        data = value.replace('\n', '<br>')
        
        return data
    else:
        return value

@register.filter(name='get_ip')
def get_ip(get_ip):
    return get_ip.ip

@register.filter(name='get_item')
def get_item(get_item):
    return get_item.name

@register.filter(name='get_nickname')
def get_nickname(get_nickname):
    if get_nickname:
        return get_nickname.nickname
    else:
        return get_nickname

@register.filter(name='get_cpu_core')
def get_cpu_core(cpu_info):
    cpu_core = cpu_info.split('* ')[1] if cpu_info and '*' in cpu_info else cpu_info
    return cpu_core

@register.filter(name='get_disk_info')
def get_disk_info(disk_info):
    try:
        disk_size = 0
        if disk_info:
            disk_dic = ast.literal_eval(disk_info)
            for disk, size in disk_dic.items():
                disk_size += size
            disk_size = int(disk_size)
        else:
            disk_size = ''
    except Exception:
        disk_size = disk_info
    return disk_size


@register.filter(name='displayName')
def displayName(value, arg):
    return apply(eval('value.get_'+arg+'_display'), ())

@register.filter(name='get_nickname')
def get_nickname(get_nickname):
    return get_nickname.nickname

@register.filter(name='get_name')
def get_name(get_name):
    return get_name.name

@register.filter(name='get_user')
def get_name(get_user):
    return get_user.name

@register.filter(name='get_app')
def get_app(get_app):
    return get_app.name

@register.filter(name='rec_str2uni')
def rec_str2uni(value):
    if value and len(value)>15:
        return value[:15]+'  ....'
    else:
        return value

@register.filter(name='sub_str2uni')
def sub_str2uni(value):
    if value and len(value)>15:
        return value[:15]+'  ....'
    else:
        return value

@register.filter(name='cont_str2uni')
def cont_str2uni(value):
    if value and len(value)>30:
        return value[:30]+'  ....'
    else:
        return value

@register.filter(name='logsub_str2uni')
def logsub_str2uni(value):
    if value and len(value)>20:
        return value[:20]+'  ....'
    else:
        return value

@register.filter(name='logcont_str2uni')
def logcont_str2uni(value):
    if value and len(value)>40:
        return value[:40]+'  ....'
    else:
        return value