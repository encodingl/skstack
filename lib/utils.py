#!/url/bin/env python
#-*- coding: utf8  -*-

import MySQLdb

from skcmdb.models import DbSource


ASSET_TYPE = (
     u"物理机",
     u"虚拟机",
     u"交换机",
     u"路由器",
     u"防火墙",
     u"Docker",
     u"其他"
    )



def mysql_execute(dbsource,sql):
    db = DbSource.objects.get(name=dbsource)
    config = {'host': db.host, 'user': db.user, 'passwd': db.password, 'port': db.port, 'db': db.db}
    db = MySQLdb.connect(charset='utf8',**config)
    cursor  = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()



