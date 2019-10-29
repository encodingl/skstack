概述
===============

该系统从py2升级到py3后 以及django1.9升级到django2.2，还在调试当中。请勿投入生产系统使用
SKSTACK主要作为运维服务台，主要提供运维相关事项登记&发布&统计、版本发布、应急预案、自动化任务执行相关功能



功能介绍
--------------------------------

主要包含功能如下：

 * 仪表盘：统计工单、用户、事件、资源相关数据
 * 工单系统：版本发布、应急预案管理、标准化运维任务工单执行
 * 用户系统：用户和菜单角色管理，工单授权、审核流程管理
 * 资源管理：软件和硬件资产管理
 * 登记管理：事件登记、FAQ、重要事项通知管理
 * 运维导航：运维值班、分工、公告、事件处理流程、相关运维系统超级链接管理
 * ANSIBLE：ansible脚本项目化管理


工单系统基本原理
--------------------------------



.. image:: _images/skw_framework.png
   :alt: image not found

.. note::
	  #. 配置中心一般指的是批量配置管理服务器如Ansible服务器，skstack可以支持多个配置中心注册到平台
	  #. 插件一般安装在配置中心，调用配置配置中心进行远程服务器实例变更或查询操作
	  #. 插件也可以安装在目标服务器实例直接执行，需要将目标服务器以配置中心的方式注册到skstack平台
	  #. 工单注册时，由管理员关联配置中心。
..

Demo
--------------------------------


Docker项目版本发布
~~~~~~~~~~~~~~~~~~~~~~

 * 基于公有云docker镜像仓库或者私有docker镜像仓库做版本仓库库管理；
 * 通过发布插件获取版本号；
 * 通过工单系统的docker项目发布插件进行版本发布

索引页面

.. image:: _images/skw_index.png
   :width: 800
   :alt: image not found
   
发布页面

.. image:: _images/skw_submmit.png
   :width: 800
   :alt: image not found
   
审计页面

.. image:: _images/skw_audit_front.png
   :width: 800
   :alt: image not found

gitlab项目版本发布
~~~~~~~~~~~~~~~~~~~~~~

 * 基于gitlab做版本仓库库管理；
 * 通过发布插件获取版本号；
 * 通过工单系统的gitlab项目发布插件进行版本发布

.. image:: _images/skw_git_submmit.png
   :width: 800
   :alt: image not found
   
压缩包项目版本发布
~~~~~~~~~~~~~~~~~~~~~~

 * 基于nginx做压缩包版本仓库管理；
 * 通过爬虫获取版本号；
 * 通过工单系统的压缩包发布插件进行版本发布

.. image:: _images/skw_tar_submmit.png
   :width: 800
   :alt: image not found


