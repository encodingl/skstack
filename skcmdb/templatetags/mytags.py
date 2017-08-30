# coding: utf-8


from django import template

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

@register.filter(name='get_nickname')
def get_nickname(get_nickname):
    if get_nickname:
        return get_nickname.nickname
    else:
        return get_nickname
