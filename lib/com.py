#coding:utf8
import ConfigParser, os
from django.conf import settings

config_path = os.path.join(settings.BASE_DIR, 'skipper.conf')

def config(path=config_path):
    obj = ConfigParser.ConfigParser()
    obj.read(path)
    return obj

cfg = config()



def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object