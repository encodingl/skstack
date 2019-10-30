#!/url/bin/env python
# -*- coding: utf8  -*-

from django.conf import settings
import MySQLdb
from skcmdb.models import DbSource

def mysql_execute(dbsource, sql):
    db = DbSource.objects.get(id=int(dbsource))
    config = {'host': db.host, 'user': db.user, 'passwd': db.password, 'port': db.port, 'db': db.db, 'charset': 'utf8'}
    db = MySQLdb.connect(**config)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data




