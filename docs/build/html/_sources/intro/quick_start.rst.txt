快速入门
===============

步骤
----------------

基本使用流程
^^^^^^^^^^^^^^^^^^^^^^

.. image:: _images/skw_steps.png
   :width: 800
   :alt: image not found
   
.. note::
	  #. 审核流程非必须，若为开启审核功能，用户提单后可以直接执行和返回执行结果
	  #. 快速入门手册没有开启审核流程，假设运维和提单人员为同一人，都用管理员账号配置。
	  #. 关于审核流程配置详见：用户手册》用户系统》审核流程配置
..

菜单和用户配置流程
^^^^^^^^^^^^^^^^^^^^^^
 
  #. 添加菜单
  #. 添加菜单角色
  #. 创建用户并授权
  #. 创建用户组

.. note::
	超级管理员默认具有所有菜单访问权限.
..

工单配置流程
^^^^^^^^^^^^^^^^^^^^^^
 
  #. 配置中心初始化
  #. 用途分类配置
  #. 工单变量注册
  #. 工单变量分组
  #. 工单插件注册
 
.. note::
	若ansible或相关插件执行服务器与skstack在同一台服务器 则不需要进行配置中心初始化工作
..







创建菜单和用户并授权
--------------------------------

添加菜单
^^^^^^^^^^^^^^^^^^^^^^
用户管理》权限管理》菜单权限》添加权限

.. image:: _images/skw_user_menupri.png
   :width: 800
   :alt: image not found
   
.. note::
	菜单权限基于URL方式认证授权，URL后需要以"/"符号结尾，详见上截图.
..


添加菜单角色
^^^^^^^^^^^^^^^^^^^^^^

用户管理》权限管理》菜单角色》添加角色
 
.. image:: _images/skw_user_menurole.png
   :width: 800
   :alt: image not found

   
添加用户和授权
^^^^^^^^^^^^^^^^^^^^^^

用户管理》用户管理》菜单角色》添加用户并授权菜单角色权限
 
	 略
   
添加用户组
^^^^^^^^^^^^^^^^^^^^^^

用户管理》群组管理》菜单角色》添加用户组
 
 略
 
.. note::
	用户组用于工单授权和审核流程层级授权
..

 

创建一个ansible任务工单
--------------------------

效果展示
^^^^^^^^^^^^^^^^^^^^^^

.. image:: _images/skw_submit_ansible.png
   :width: 800
   :alt: image not found
   
.. note::
	  #. AnsibleCMD为用户需要输入的shell命令
	  #. AnsibleHosts为用户选择需要执行shell命令的目标主机
	  #. 执行结果将基于xterm样式 websocket实时输出
..
   
插件环境基础配置
^^^^^^^^^^^^^^^^^^^^^^  
 
#. ansible安装：略
#. 插件安装：git clone 《插件git url》，注意：插件安装到ansible服务器
#. 安装python2.7的python虚拟环境：略；该插件
#. 配置demo1作为ansible 远程执行命令的客户机 作为测试：略




ansible cmd插件测试
^^^^^^^^^^^^^^^^^^^^^^

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



添加配置中心
^^^^^^^^^^^^^^^^^^^^^^

.. note::
	  #. 若ansible或相关插件执行服务器与skstack在同一台服务器 则不需要进行配置中心添加工作
	  #. skstack和ansible和插件工具工作原理，详见快速入门 概述章节内容。
	  #. skstack支持添加多个配置中心：如不同环境使用不同的ansible作为配置管理服务器。
..

工单系统》配置》配置中心》添加

.. image:: _images/skw_conf_center.png
   :width: 800
   :alt: image not found
   


添加完毕点击验证按钮能够获取到配置中心时间表示配置成功，如下截图

.. image:: _images/skw_conf_center_ver.png
   :width: 800
   :alt: image not found

添加用途分类
^^^^^^^^^^^^^^^^^^^^^^

.. image:: _images/skw_conf_category.png
   :width: 800
   :alt: image not found

工单变量注册
^^^^^^^^^^^^^^^^^^^^^^

| 该处用于注册工单外部变量，通过脚本或者管理员自定义的方式获取变量参数，通过web交互界面由用户传递给工单任务脚本
| 注册ansible hosts变量，用于执行asnible cmd时候 选择主机，如web效果展示的AnsibleCMD选项

.. image:: _images/skw_conf_var_reg1.png
   :width: 800
   :alt: image not found
   
   
.. image:: _images/skw_conf_var_reg2.png
   :width: 800
   :alt: image not found
   
注册自定义文本输入框变量，用于输入shell命令，如web效果展示的AnsibleHosts选项

.. image:: _images/skw_conf_var_reg3.png
   :width: 800
   :alt: image not found
   
   
.. image:: _images/skw_conf_var_reg4.png
   :width: 800
   :alt: image not found

工单变量分组
^^^^^^^^^^^^^^^^^^^^^^

每个工单可以关联一组外部变量，只有加入改组的工单变量，才能在web交互界面提单时进行选择。

.. image:: _images/skw_conf_var_group.png
   :width: 800
   :alt: image not found

工单插件注册
^^^^^^^^^^^^^^^^^^^^^^

.. image:: _images/skw_conf_wo1.png
   :width: 800
   :alt: image not found
   
.. image:: _images/skw_conf_wo2.png
   :width: 800
   :alt: image not found
   
.. image:: _images/skw_conf_wo3.png
   :width: 800
   :alt: image not found

.. note::
	#. 每定义一个任务工单，可以传递外部list变量（用户可选）和内部变量（对用户不可见）给工单
	#. 内部变量此处未用，格式为dict 如{"GitProjName":"app01"} key为变量名，value为值，可以定义多个kv
	#. 外部和内部变量通过"{变量名}" 传递给任务脚本；如 ansible_cmd.py -e prod -g "{AnsibleHosts}" -c "{AnsibleCMD}"
	
..


