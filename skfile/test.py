#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
path = ["/etc/ansible/project","/data/deploy/config"]
dirList=[] #所有目录
fileList=[] #所有目录下返回的文件列表
for dir in path:
   print dir
   files = os.listdir(dir)
   for f in files:
      if(os.path.isdir(f)):
         if(f[0]=='.'):
               pass
         else:
              dirList.append(f)
      if(os.path.isfile(f)):
         fileList.append(f)
print dir, dirList,fileList

