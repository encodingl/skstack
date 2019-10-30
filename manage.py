#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skstack.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
