工单系统
===============

请先参考快速入门手册，后续补充该章节内容


原理
----------------

详见快速入门手册概述部分

管理员配置手册
----------------

详见快速入门手册demo章节


基础配置
~~~~~~~~~~~~~~~~~~~~~~

  #. 环境分类：如PROD表示生产环境，STAGE表示准生产环境，激活的工单应该归属其中一个环境分类，用户提单的时候可以在提单页面该环境标签下找到相应的工单
  #. 用途分类：为每个类型的项目单独创建一个分类，比如docker项目创建创建DeployDocker分类；git静态文件项目创建DeployGit分类


配置中心
~~~~~~~~~~~~~~~~~~~~~~

参考 :ref:`示例快速入门配置中心 <config-center>`.


变量配置
~~~~~~~~~~~~~~~~~~~~~~

每定义一个任务工单，可以传递外部可选变量（用户可选）和内部变量（对用户不可见）给工单

可选变量
""""""""""""""""""""""""


 * 通过变量注册的方式定义，通过外部脚本或者管理员定义。格式为list ，如 ["host1","host2","host3"]
 * 脚本获取，通过变量获取脚本动态获取可选变量。 :ref:`示例docker发布插件项目变量 <user-vars>`.
 * 管理员定义，管理员可以定义一个变量并提供一组参数给用户选择。 :ref:`实例docker发布插件执行模式变量 <user-vars>`.

内部变量
""""""""""""""""""""""""

 * 新增工单时编辑内置变量定义
 * 格式为dict 如{"GitProjName":"app01"} key为变量名，value为值
 * 内部变量主要用于静态变量，不会动态更新，默认可为空

变量传递
""""""""""""""""""""""""

 * 内部变量和外部变量都通过"{变量名}" 传递给任务脚本；
 * 如 python main_deploy_git.py -e prod -g "{GitProjName}" -i "{AnsibleHosts}"


用户使用手册
----------------



提单
~~~~~~~~~~~~~~~~~~~~~~

| 由已授权提单权限用户使用，若工单开启审核，提交工单后，需等待完成审核流定义的各层级完成审核后 才能到执行菜单界面 执行工单，将图1
| 若没有开启审核，可以在提单页面直接执行工单,将图2

图1

.. image:: _images/submit_only.png
   :alt: image not found

.. note::
	  #. 提交成功后显示submited successful，表示提交成功，需要审核通过后才能进入执行页面执行任务。

图2

.. image:: _images/submit_all.png
   :alt: image not found
   
.. note::
	  #. 提交成功后显示finished successful表示发布成功
   
审核
~~~~~~~~~~~~~~~~~~~~~~

由审核人员使用，工单开启审核后，需要通过审核流程中所定义审核流程才能执行。拒绝必须填写拒绝理由，同意可以不填 意见，直接点击同意按钮
进入审核页面如下：

.. image:: _images/audit_index.png
   :alt: image not found

点击同意后：拒绝必须给出拒绝理由，同意可以不用填意见

.. image:: _images/audit_permit.png
   :alt: image not found
   
查看详情

.. image:: _images/audit_permit.png
   :alt: image not found

执行
~~~~~~~~~~~~~~~~~~~~~~

审核通过后，已授权提单用户可以到该页面选择提交的工单并执行

进入执行索引页面：

.. image:: _images/deploy_index.png
   :alt: image not found

进入项目执行界面：

.. image:: _images/deploy_result.png
   :alt: image not found


审计
~~~~~~~~~~~~~~~~~~~~~~

这里记录所有工单执行历史，具有访问该菜单权限的用户，可以查看所有执行记录，包含其他用户的执行记录，以便于进行历史版本查看

.. image:: _images/history.png
   :alt: image not found

.. note::
	  #. 历史记录审计页面当前所有提交记录都记录在前台任务页面，后台任务模块暂未release。

