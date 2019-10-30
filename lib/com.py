#coding:utf8
import configparser, os
from django.conf import settings

configfile = settings.CONFIGFILE

def config(path=configfile):
    obj = configparser.ConfigParser()
    obj.read(path)
    return obj

cfg = config()


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in list(kwargs.values()):
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object