====================================
SKSTACK |version| documentation
====================================

.. SKSTACK documentation master file, created by
   sphinx-quickstart on Thu Oct 24 18:33:14 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



快速入门
====================================

.. toctree::
   :caption: 快速入门
   :maxdepth: 3
   :numbered:
   :hidden:


   intro/overview
   intro/install
   intro/quick_start
   intro/release_info
   
:doc:`intro/overview`

.. note::
	 该项目目前处于内测阶段，暂未开源，请其他渠道获取代码的童鞋 暂未投入生产使用
..

:主要包含功能如下:

 * 仪表盘：统计工单、用户相关数据统计
 * 工单系统：工单提交、审核、发布、审计
 * 用户系统：用户和菜单角色管理，工单授权、审核流程管理
 * 系统管理：管理员使用ansible hosts索引、后台任务监控


:doc:`intro/install`

    SKSTACK平台手动安装文档.

:doc:`intro/quick_start`

    该章节通过几个场景的配置介绍，使用户能够快速使用skstack平台。
    
:doc:`intro/release_info`

    版本更新说明


  


用户手册
====================================

.. toctree::
	:caption: 用户手册
	:maxdepth: 3
	:numbered: 
	:hidden:
	
	
	admin/skaccounts
	admin/skworkorder
	admin/skconfig

   
:doc:`admin/skaccounts`

    用户系统配置手册，介绍用户、菜单权限、审核流程相关配置.

:doc:`admin/skworkorder`

    | 工单系统针针对管理员角色介绍版本发布管理，工单插件、变量、交互界面配置等；
    | 针对使用者介绍提单、审核、执行、历史查看各环节使用说明

:doc:`admin/skconfig`

    系统配置模块介绍ansible hosts索引页面、celery-flower定时任务监控页面配置和查看

插件使用手册
====================================

.. toctree::
	:caption: 插件使用手册
	:maxdepth: 3
	:numbered: 
	:hidden:
	
	plugins/overview
	plugins/docker_deploy
	plugins/git_deploy
	plugins/package_deploy
	plugins/ansible_deploy
	plugins/the_third
   
   
:doc:`plugins/overview`

  官方插件使用概述
    
:doc:`plugins/docker_deploy`

    介绍Docker部署插件的使用方式
    
:doc:`plugins/git_deploy`

    介绍git静态文件部署插件的使用方式
    
:doc:`plugins/package_deploy`

    介绍基于nginx作为仓库静态文件版本部署插件的使用方式

:doc:`plugins/ansible_deploy`

    介绍基于 ansible 部署 shell 和 playbook 插件的使用方式

:doc:`plugins/the_third`

    第三方插件索引，暂未收录



开发者指南
====================================

.. toctree::
	:caption: 开发者指南
	:maxdepth: 3
	:numbered: 
	:hidden:
	
	dev/demodoc
	dev/plugins
	dev/web
	dev/git_guidelines
	dev/author_info
	dev/join_us
   
:doc:`dev/demodoc`

    文档编写指南.
    
:doc:`dev/plugins`

    介绍插件目录、脚本、库文件、配置文件、日志文件命名规范和使用规范,未完成
    
:doc:`dev/web`

    SKSTACK web平台相关开发规范，如：命名规范 api规范 日志规范等。
    
:doc:`dev/git_guidelines`

    SKSTACK web平台git功能分支开发和版本管理指南。
    
:doc:`dev/author_info`

    平台和插件主要开发人员介绍
    
:doc:`dev/join_us`

    暂未开放
