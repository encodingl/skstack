.. _dev-skplugins:

插件开发指南
==============================

| skstack平台的插件注册不限制开发语言，理论支持所有能在linux服务器命令行界面直接运行的脚本。
| 本文档主要基于python说明，其他语言请尽量遵循示例相关目录、文件命名和日志规范
| 优先使用python3.7 开发与skstack版本保持一致。



概述
==============================

| skstack插件库主要配合skstack web平台的工单系统使用，结合skstack工单系统，可以实现工单审核和自动化执行等功能；插件也可以作为独立的脚本使用。
| skstack官方插件基于python开发，所有官方插件均遵循下文中定义的目录和命名规范
| skstack官方插件的python版本与skstack web平台的python版本保持一致。
| skstack每个官方插件包含如下脚本和文件

#. 前置任务脚本：对应工单系统的前置任务配置项，是主任务执行之前先执行的任务脚本，一般用来做一些前置检查；非必须项
#. 主任务脚本：对应工单系统的主任务配置项目，是主要任务功能脚本；必须项
#. 后置任务脚本：对应工单系统的后置任务配置项，主任务执行成功后的，会执行后置任务脚本；非必须项
#. 变量获取脚本：用于工单系统交互界面获取可选list变量；非必须；
#. 子任务脚本：用于给前置、主、后置任务调用的脚本，不会单独执行。
#. 配置文件：各脚本读取的配置参数，必须项
#. 私有库和模块：各脚本共用的模块，非必须

工作原理
--------------------------------

.. image:: /intro/_images/skstack_workflow.png
   :alt: image not found

.. note::
	  #. 前置任务未非必须项，若没有会跳过改执行步骤
	  #. 后置任务未非必须项，若没有会跳过改执行步骤
	  #. 只有变量注册为通过变量脚本获取的可选变量时才会执行变量获取脚本。没有则跳过该步骤
..


安装步骤
--------------------------------
#. 下载插件库：git clone <skstack_plugins_git_url>
#. 安装python 虚拟机：略。tips：若已安装skstack web系统，请忽略该步骤，直接使用skstack web平台的python虚拟机即可
#. 安装依赖库：切换到skstack python虚拟机执行 pip install -r requirements.txt

目录规范
--------------------------------

插件库主目录介绍

.. code-block::	bash

	(skstack) [root@registry soft]# tree -d skstack_plugins
	skstack_plugins      #插件库主目录
	├── conf_pub			#插件库公共配置文件目录，如日志路径定义参数
	├── lib_pub				#插件库公共库文件和函数模块位置，如日志格式化函数，配置文件加载函数
	├── pl_ansible			#ansible功能插件主目录
	│   ├── conf			#所属功能插件配置文件目录
	│   └── lib_pri			#所属功能插件私有库目录，该功能插件多个脚本可以共用的私有函数和类保存到该文件夹
	├── pl_deploy_docker    #docker部署功能插件主目录
	│   └── conf
	├── pl_deploy_git		#git部署功能插件主目录
	│   ├── conf
	│   ├── lib_pri
	└── pl_deploy_package	#压缩包部署功能插件主目录
	    ├── conf
	    ├── lib_pri
	    


公共配置文件配置说明
--------------------------------

| 配置参数通过json文件里面定义的字典方式进行引用
| 公共配置文件目前版本只定义所有官方插件的日志根路径
| 最佳实践为不同环境单独使用一个配置文件，如生产配置文件prod_conf.json 使用demo.json复制 
| 配置文件强制遵循命名规范，必须以"_conf.json"结尾，否则各插件无法应用

::
	
	(skstack) [root@registry skstack_plugins]# tree conf_pub/
	conf_pub/
	├── demo.json
	├── prod_conf.json
	└── stage_conf.json

	(skstack) [root@registry skstack_plugins]# more conf_pub/demo.json
	{
	        "log_path":"/opt/sklogs/"   #定义所有插件的日志根目录
	}



功能插件目录和文件说明
--------------------------------
以git部署插件为例说明
 
::

	[root@registry skstack_plugins]# tree pl_deploy_git/
	pl_deploy_git/				#插件主目录
	├── conf					#插件配置文件目录
	│   ├── demo.json			#示例配置文件
	│   ├── prod_conf.json		#prod环境配置文件，
	│   └── stage_conf.json		#stage环境配置文件
	├── __init__.py
	├── lib_pri
	│   ├── git.py
	├── main_git_deploy.py		#主任务脚本
	├── pre_git_pull.py			#前置任务脚本
	├── sc_static_sync.yml		#被调用的任务脚本
	└── var_git_commit_id.py	#变量获取脚本

命名规范
--------------------------------

#. 插件目录命名：加pl_前缀
#. 前置任务脚本：加pre_前缀,
#. 主任务脚本：加main_前缀
#. 后置任务脚本：加post_前缀
#. 变量获取脚本：加var_前缀
#. 配置文件命名：加_conf.json后缀
#. 脚本文件命名：加sc_前缀；脚本文件主要用于主任务脚本调用
#. 私有库目录：lib_pri；私有库函数主要用于主任务脚本或者sc_脚本调用
#. 日志文件命名："插件主目录名称+.log" ;如pl_deploy_git.log




脚本传参规范
------------------------------

脚本传参：脚步外部参数传递通过argparse模块功能方式实现 ，如下4个通过argparse模块定义的引入参数关键字，为了保持与现有官方插件一致性，请保持命名一致

#. -h 帮助文档
#. -e 指定配置文件，一般每个环境单独使用一个配置文件，详见各插件最佳实例
#. -p 指定需要操作的项目名字，该项目必须存在于指定配置文件当中
#. -a 指定项目所在的目标主机，若为空则读取ansbile hosts文件中 与项目名一致的group。



配置文件规范
------------------------------
用于python插件开发，其他语言请参考命名规范

#. 配置参数读取：对于生产、测试、stg相关环境的配置文件变量不能硬编码到变量获取脚本或者任务脚本文件中
#. 配置文件读取：应该从conf中相应的配置文件中动态获取，通过 “-e”参数指定环境，去读不同环境下的配置文件；不同环境下的配置文件通过命名后缀区分
#. 前端复选框当只选一个的时候传递值为字符串，超过一个选项传递值为list，需要在脚本中做判断具体参考插件特殊情况处理 复选框处理示例

日志规范
------------------------------

#. 格式：日期 日志级别 消息，示例：2019-12-23 09:05:31.023 INFO Note: checking out '953f4f1'.
#. ansible日志：ansible任务的执行保持与ansible本身日志一致，不用加时间戳和消息级别
#. 日志模块引入：统一使用官方日志模块：from lib_pub.logger import 如下两个日志模块
	- sklog_original（不包含时间戳和日志级别，一般用于ansible任务日志）
	- sklog_init（包含时间戳和日志级别一般用于非ansible日志） 
	- 日志模块用法参考现有官方插件




插件特殊情况处理
------------------------------

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
