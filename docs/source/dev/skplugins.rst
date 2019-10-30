插件开发指南1.0
==============================

| 本规范仅适用于python2.7开发的已发布项目维护。新的插件开发请参考 :ref:`插件开发指南2.0 <dev-skplugins2>`
| skstack平台，理论支持所有能在linux服务器命令行界面直接运行的语言。
| 本文档主要基于python说明，其他语言可以参考相关目录、文件命名和日志规范


目录规范
------------------------------

::

   skPlugins/            #插件主目录
   |-- conf                 #配置文目录
   |   |-- ansible_conf_dev.py
   |   |-- ansible_conf_prod.py
   |   |-- ansible_conf_stg.py
   |   |-- redis_conf_dev.py
   |   |-- redis_conf_prod.py
   |   |-- redis_conf_stg.py
   |-- lib  #插件公共库目录
   |-- scPublic  #公共插件目录
   |   |-- vars_get_ansibleHostsGroup.py
   `-- scRedis  #redis插件目录
       `-- redis_getkeyvalue_main.py

.. warning::
	后续版本配置文件和lib文件将统一存放于所属插件主目录
..

命名规范
------------------------------

#. 插件目录命名：sc前缀加分类名称(分类名首字母大写) 例如scRedis
#. 配置文件命名：配置文件用途加“\ *conf*\ 环境简称”后缀 ,例如：
   ansible\ *conf*\ prod.py
#. 变量获取脚本：vars前缀加用途，例如：vars\ *get*\ ansibleHostsGroup.py
#. 工单任务脚本：任务名称+任务用途。 任务用途main：表示主任务脚本
   举例：redis\ *getkeyvalue*\ main.py pre：表示前置任务脚本
   post：表示后置任务脚本

脚本编写规范和配置文件规范
------------------------------

#. 对于生产、测试、stg相关环境的配置文件变量不能硬编码到变量获取脚本或者任务脚本文件中
#. 配置文件应该从conf中相应的配置文件中动态获取，通过 “-e”参数指定环境，去读不同环境下的配置文件；不同环境下的配置文件通过命名后缀区分
#. 脚步外部参数传递通过OptionParser模块功能方式实现 参考如下文demo实例 
#. 前端复选框当只选一个的时候传递值为字符串，超过一个选项传递值为list，需要在脚本中做判断具体参考demo 复选框处理示例


插件Demo
------------------------------

ansible shell模块执行插件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| 确认先在命令行模式测试插件是否工作正常，不同的插件详见各插件使用说明文档，demo以ansible cmd插件脚本为例；
| 确认ansible cmd脚本"ansible_cmd.py"的配置文件配置正确

.. code-block:: console
	:emphasize-lines: 4
	
	(skplugins) [root@devops scAnsible]# more ../conf/ansible_conf_dev.py
	#! /usr/bin/env python
	# -*- coding: utf-8 -*-
	ansible_hosts_file = "/etc/ansible/hosts"
	
	

.. code-block:: console

	(skplugins) [root@devops scAnsible]# python ansible_cmd.py -e dev -g demo1 -c date
	svn | CHANGED | rc=0 >>
	2019年 10月 28日 星期一 15:27:26 CST
	(skplugins) [root@devops scAnsible]# python ansible_cmd.py -h
	Usage: ansible_cmd.py [options]
	
	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -e [prod|stg|...], --environment=[prod|stg|...]
	                        input the environment in which the script needs to be
	                        executed
	  -g [gp01|ip|...], --group=[gp01|ip|...]
	                        input the ansible hosts group
	  -c [ls|cd|...], --command=[ls|cd|...]
	                        input the command
	(skplugins) [root@devops scAnsible]# ll
	总用量 12
	-rwxr-xr-x. 1 root root 1672 7月   8 12:02 ansible_cmd.py
	-rwxr-xr-x. 1 root root 1492 6月   5 11:47 ansible_playbook.py
	-rw-r--r--. 1 root root    0 5月  21 17:19 __init__.py
	-rwxr-xr-x. 1 root root 1494 5月  21 17:19 vars_get_AnsibleHosts.py
	(skplugins) [root@devops scAnsible]#
	
.. note::
	该处--e为预留参数，该脚本没有使用，后续将用于不同环境的配置文件读取
..


确认ansible hosts变量获取脚本工作正常

.. code-block:: console

	(skplugins) [root@devops scAnsible]# python vars_get_AnsibleHosts.py -e dev
	['appT_h5', 'app_h5', 'demo1', 'dev_nginx', 'mitrade-cloud-config-repo', 'skplugins', 'system-hosts-file', 'web-cms-app', 'webtrader', 'webtrader2']
	(skplugins) [root@devops scAnsible]# python vars_get_AnsibleHosts.py -h
	Usage: vars_get_AnsibleHosts.py [options]
	
	Options:
	  --version             show program's version number and exit
	  -h, --help            show this help message and exit
	  -e [prod|stg|...], --environment=[prod|stg|...]
	                        input the environment in which the script needs to be
	                        executed
	        
	
.. note::
	该处-e参数为获取不同环境的配置文件参数；执行结果返回看到ansible hosts里面定义的group列表即为正常
..

获取redis键值对
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

任务脚本文件：redis\ *getkeyvalue*\ main.py

.. code-block:: python

   #! /usr/bin/env python
   #-*- coding: utf-8 -*-

   #Import the base library for the script
   import sys
   from optparse import OptionParser
   import os
   #Import the skplugins modules
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.append(BASE_DIR)

   #Start from here to import the other libraries that the script needs
   import redis

   def parseOption(argv):
       parser = OptionParser(version="%prog 1.0.0")
       parser.add_option("-i", "--redis-instance", dest="instance", metavar="[DomainName|ip]",
                           help="input the redis instance IP or domain name you want to query")
       parser.add_option("-k", "--redis-key", dest="key", help="input the redis key you want to query",
                           metavar="[redis-key]")
       parser.add_option("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                           metavar="[prod|stg|...]")
       (options, args) = parser.parse_args()
       if not len(argv): parser.print_help();sys.exit(1) 
       return options 

   def main(argv):
       options = parseOption(argv)
       config_file = "redis_conf_"+options.env
       exec("from conf."+config_file+ " import redis_vars")
       redis_host = options.instance
       redis_port = redis_vars[options.instance]["port"]
       redis_password = redis_vars[options.instance]["password"]
       ins1 = redis.Redis(host=redis_host,port=redis_port,password=redis_password)
       key_value = ins1.get(options.key) 
       print key_value
       
   if __name__ == "__main__":
       main(sys.argv[1:])

变量配置文件 redis\ *conf*\ stg.py


.. code-block:: python

      #! /usr/bin/env python

   redis_vars={
   "i1.test.com":{"port":6379,"password":"12=ddfdfdfd",},
   "192.168.67.13":{"port":6379,"password":"o29OCVEddtA"},
   }

执行效果


.. code-block:: python

   (venv-skplugins) [root@localhost scRedis]# python redis_getkeyvalue_main.py -h
   Usage: redis_getkeyvalue_main.py [options]

   Options:
     --version             show program's version number and exit
     -h, --help            show this help message and exit
     -i [DomainName|ip], --redis-instance=[DomainName|ip]
                           input the redis instance IP or domain name you want to
                           query
     -k [redis-key], --redis-key=[redis-key]
                           input the redis key you want to query
     -e [prod|stg|...], --environment=[prod|stg|...]
                           input the environment in which the script needs to be
                           executed
   (venv-skplugins) [root@localhost scRedis]# 
   (venv-skplugins) [root@localhost scRedis]# python redis_getkeyvalue_main.py -i "i1.test.com" -k "ProductInfo" -e stg
   None

   


复选框模式传参处理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    #! /usr/bin/env python
   # -*- coding: utf-8 -*-


   import sys
   from optparse import OptionParser
   import os

   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.append(BASE_DIR)

   def parseOption(argv):
       parser = OptionParser(version="%prog 1.0.0")
       parser.add_option("-m", "--multiple-vars", dest="mul", metavar="[variable_name]",
                           help="used to print the multiple select form variables")
       
       parser.add_option("-s", "--single-var", dest="single", metavar="[variable_name]",
                           help="used to print the sigle select form variable")
       
       parser.add_option("-i", "--inner-var", dest="inner", metavar="[variable_key]",
                           help="used to print the inner variable key value")
       
       (options, args) = parser.parse_args()
       if not len(argv): parser.print_help();sys.exit(1) 
       return options 

   def main(argv):
       options = parseOption(argv)
       inner_var = options.inner
       print "inner_var:%s" % inner_var
       multiple_vars = options.mul
       # options.mul 为复选框当只选一个的时候传递值为字符串，超过一个选项传递值为list，需要在脚本中做判断
       if isinstance(multiple_vars, list):
           multiple_vars = eval(options.mul)
           
           for i in multiple_vars:
               print "multiple_vars:%s" % i
       else:
           print "multiple_vars:%s" % multiple_vars
       single_var = options.single
       print "single_var:%s" % single_var

   if __name__ == "__main__":
       main(sys.argv[1:])
       
插件返回子进程异常处理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| 如果插件子进程执行异常，且子进程返回给插件父进程的状态吗为非0，但是插件父进程执行完毕返回的状态码为0，这种情况下需要在父进程主动抛出异常，方便sk平台捕获
| 获取更准确的执行结果，示例如下：

1 子进程异常但是父进程正常：

.. code-block:: console

   (skipper) [root@localhost scAnsible]# ./ansible_cmd.py -g gtest -c date1
   yw108 | FAILED | rc=2 >>

   [Errno 2] 没有那个文件或目录

   yunwei61 | FAILED | rc=2 >>

   [Errno 2] 没有那个文件或目录

   (skipper) [root@localhost scAnsible]# echo $?
   0

2 改造后脚本如下，子进程异常主动抛出异常

.. code-block:: python

     #! /usr/bin/env python
   # -*- coding: utf-8 -*-
   from optparse import OptionParser
   import sys
   import os
   from subprocess import Popen, PIPE, STDOUT, call
   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   sys.path.append(BASE_DIR)

   import re

   def parseOption(argv):
       parser = OptionParser(version="%prog 1.0.0")
       parser.add_option("-e", "--environment", dest="env", help="input the environment in which the script needs to be executed ",
                           metavar="[prod|stg|...]")
       parser.add_option("-g", "--group", dest="group", help="input the ansible hosts group",
                           metavar="[gp01|ip|...]")
       parser.add_option("-c", "--command", dest="cmd", help="input the command",
                           metavar="[ls|cd|...]")
      
       (options, args) = parser.parse_args()
       if not len(argv): parser.print_help();sys.exit(1) 
       return options 

   def ansible_cmd_func(hosts,forks,cmd):
       ansible_cmd = "ansible %s -f %s  -a %s" % (hosts,forks,cmd) 

       try:        
           pcmd = Popen(ansible_cmd, stdout=PIPE, stderr=PIPE, shell=True) 
           while True: 
               line = pcmd.stdout.readline().strip()  #获取内容
               if line:
                   print line
               else:
                   break   
           
       except:
           exinfo=sys.exc_info()
           print exinfo
       
       retcode = pcmd.wait()
       if retcode == 0:
           pass
       else:
       #子进程异常主动抛出异常
           raise Exception("命令执行失败")
   def main(argv):
       options = parseOption(argv)
       hosts = options.group
       forks = 5
       cmd = options.cmd
       ansible_cmd_func(hosts,forks,cmd)
    
       

   if __name__ == "__main__":
       main(sys.argv[1:])

3 主动抛出异常后执行结果如下：

.. code-block:: console

    (venv-adminset) [root@localhost scAnsible]# ./ansible_cmd.py -g gtest -c date1
       yw108 | FAILED | rc=2 >>
       [Errno 2] 没有那个文件或目录
       yunwei61 | FAILED | rc=2 >>
       [Errno 2] 没有那个文件或目录
       Traceback (most recent call last):
         File "./ansible_cmd.py", line 56, in <module>
           main(sys.argv[1:])
         File "./ansible_cmd.py", line 51, in main
           ansible_cmd_func(hosts,forks,cmd)
         File "./ansible_cmd.py", line 45, in ansible_cmd_func
           raise Exception("命令执行失败")
       Exception: 命令执行失败
       (venv-adminset) [root@localhost scAnsible]# echo $?
       1