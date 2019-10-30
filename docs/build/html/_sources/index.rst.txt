====================================
SKSTACK |version| documentation
====================================

.. SKSTACK documentation master file, created by
   sphinx-quickstart on Thu Oct 24 18:33:14 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



快速入门
==================

.. toctree::
   :caption: 快速入门
   :maxdepth: 3
   :numbered:
   :hidden:


   intro/overview
   intro/install
   intro/quick_start
   
:doc:`intro/overview`

	该系统从py2升级到py3后 以及django1.9升级到django2.2，还在调试当中。请勿投入生产系统使用

:doc:`intro/install`

    SKSTACK平台手动安装文档.

:doc:`intro/quick_start`

    该章节通过几个场景的配置介绍，使用户能够快速使用skstack平台。


  


用户手册
==================

.. toctree::
 :caption: 用户手册
 :maxdepth: 3
 :numbered: 
 :hidden:

 
 admin/skaccounts
 admin/skworkorder

   
:doc:`admin/skaccounts`

    用户系统配置手册，介绍用户、菜单权限、审核流程相关配置.

:doc:`admin/skworkorder`

    | 工单系统针对管理员介绍版本发布管理，工单插件、变量、交互界面配置；
    | 针对使用者介绍提单、审核、执行、历史查看各环节使用说明



插件使用手册
==================

.. toctree::
 :caption: 插件使用手册
 :maxdepth: 3
 :numbered: 
 :hidden:

 
 plugins/docker_deploy
 plugins/static_deploy
   
:doc:`plugins/docker_deploy`

    介绍Docker部署插件的使用方式
    
:doc:`plugins/static_deploy`

    介绍静态文件部署插件的使用方式
   

开发者指南
==================

.. toctree::
 :caption: 开发者指南
 :maxdepth: 3
 :numbered: 
 :hidden:


 dev/demodoc
 dev/skplugins
 dev/skplugins2
 dev/web
   
:doc:`dev/demodoc`

    文档编写指南.

:doc:`dev/skplugins`

    适用于已发布项目维护，新项目插件开发请参考2.0；
    
:doc:`dev/skplugins2`

    介绍插件目录、脚本、库文件、配置文件、日志文件命名规范和使用规范
    
:doc:`dev/web`

    SKSTACK web平台相关开发规范，如：命名规范 api规范 日志规范等。
