Tar.gz文件部署插件使用指南
====================================

概述
--------------------------------

压缩包部署插件，主要用于部署tar.gz压缩包静态文件项目，压缩包以版本命名的方式，存放到nginx特定目录。
发布插件通过爬虫获取nginx中对应的项目版本，并拉取下来部署到目标服务器。



*版本管理*

- 基于nginx web仓库，将对应版本文件release到nginx对应目录，并开启nginx autoindex参数，发布插件通过爬虫获取版本号







目录说明
--------------------------------

.. code-block::	bash
		
	pl_deploy_package/		#插件主目录
	├── conf				#配置文件目录
	│   ├── demo.json		#配置文件模板
	├── lib_pri
	│   ├── func.py
	├── main_static_deploy.py	#主任务脚本，用于将项目文件同步到目标服务器
	├── pre_package_download.py	#前置任务脚本，用于将对应版本的项目文件从nginx上下载下来
	├── sc_static_sync.yml		#主任务模块调用的ansible playbook，用来同步文件到目标服务器使用
	└── var_package_version.py	 #变量获取脚本，用于获取对应项目在nginx上的版本清单。
	


配置文件说明
--------------------------------

demo.json为例

.. code-block:: python

	{
	
		"proj1":{  #项目名称，发布插件爬虫将以此项目名称关键字匹配包含此关键字的对应项目文件。
			 "type":"local_owner",   #项目类型：目前只支持tar和local_owner两种类型。详见note说明
			 "hosts": "demo1",	#指定需要部署到目标主机的ansible hosts group
			 "repo_url": "http://nginx_host/tarbase/proj1",  #项目nginx仓库地址
			 "proj_local_path":"/opt/tarsource/proj1/",     #项目解压到本地仓库的路径
			 "deploy_src_path":"/opt/tarsource/proj1/",     #需要同步到目标服务器的项目本地源文件路径
			 "deploy_dest_path":"/nginx_root_path/proj1/",  #项目目标服务器路径
			 "rsync_opts":[],  			#排除项指定无需同步的文件，必须指定为list类型，格式见proj2；空list表示没有文件排除，整个源目录同步，.
			 "delete_enable":"no",      #是否删除目标服务器目录存在而源目录不存在的文件。
			 "owner": "nginx",			#文件和目录所属系统用户权限
			 "group": "nginx"},			#文件和目录所属系统用户组权限
		
		"proj2":{
			 "type":"tar",
			 "hosts": "none",	
			 "repo_url": "http://nginx_host/tarbase/proj2",
			 "proj_local_path":"/opt/tarsource/proj2/",
			 "deploy_src_path":"/opt/tarsource/proj2/sub1/",
			 "deploy_dest_path":"/nginx_root_path/proj2/",
			 "rsync_opts":["--no-motd","--exclude=RedisConnect.php","--exclude=config","--exclude=runtime"],
			 "delete_enable":"no",
			 "owner": "nginx",
			 "group": "nginx"}
	
	}



.. note::
	  #. repo_url：使用插件之前需要用户先配置好nginx版本仓库，一般由研发根据版本命名规则打包并上传到nginx下指定项目命名的文件夹下。
	  #. hosts：若显示指定为none，这插件会读取插件所在服务器的ansible hosts文件中group等于项目名的目标主机，若无则报错，建议在json文件中指定
	  #. type：tar类型表示先同步文件到目标服务器再修改权限；local_owner表示，先修改权限再同步文件到目标服务器。一般情况下建议使用tar类型
	  #. rsync_opts：参数定义参考ansible playbook synchronize模块的rsync_opts参数定义

..

脚本说明
--------------------------------

变量获取脚本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

如果使用默认latest标签发布docker项目，一个工单可以只关联一个项目，也可以通过项目变量获取脚本关联多个项目

.. code-block::	bash

	(skstack) [root@ansible pl_deploy_package]# python var_package_version.py -h
	usage: pre_package_download.py [-h] [-p [proj1|proj2]] [-e [prod|stage|dev]]
                               [-f [file_name]]

	version 2.0.0
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -p [proj1|proj2], --project-name [proj1|proj2]
	                        the project name you want to depoly
	  -e [prod|stage|dev], --environment [prod|stage|dev]
	                        the environment you need deploy
	  -f [file_name], --file-name [file_name]
	                        the file name you want to depoly


.. note::
	  #. -p 指定项目名称，详见最佳实例
	  #. -e 指定配置文件，一般每个环境单独使用一个配置文件，详见最佳实例

..

主任务脚本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::	bash

	(skstack) [root@ansible pl_deploy_package]# python main_static_deploy.py -h
	usage: main_static_deploy.py [-h] [-p [proj1|proj2]] [-e [prod|stage|dev]]
	                             [-a [ansible-hosts]]
	
	version 2.0.0
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -p [proj1|proj2], --project-name [proj1|proj2]
	                        the project name you want to depoly
	  -e [prod|stage|dev], --environment [prod|stage|dev]
	                        the environment you need deploy
	  -a [ansible-hosts], --ansible-hosts [ansible-hosts]
	                        the destination hosts you want to depoly

	(skstack) [root@ansible pl_deploy_package]#
		
.. note::
	  #. -e 指定配置文件，一般每个环境单独使用一个配置文件，详见最佳实例
	  #. -p 指定需要操作的git项目名字，该项目必须存在于指定配置文件当中
	  #. -a 指定项目所在的目标主机，若为空则读取ansbile hosts文件中 与项目名一致的group。
..	





Web模式示例
--------------------------------

提单页面如下：

.. image:: _images/tar_submit.png
   :alt: image not found

.. note::
	  #. 获取版本按照文件名倒序排序；

结果页展示：

.. image:: _images/tar_result.png
   :alt: image not found
   
.. note::
	  #. 结果页面，参考ansible结果日志


 

命令行模式脚本示例
--------------------------------

项目变量获取

.. code-block::	bash
 
	(skstack) [root@ansible pl_deploy_package]# python var_package_version.py -e dev -p proj1
	['proj1-201909270820.tar.gz', 'proj1-201909270746.tar.gz', 'proj1-201908190124.tar.gz']


	
.. note::
	  #. 如上表示从-e表示从dev_conf.json 配置文件读取 包含proj1关键字的项目，返回结果为list，根据文件名倒序进行排序

	  
	  
前置任务脚本

.. code-block::	bash

	(skstack) [root@ansible pl_deploy_package]# python pre_package_download.py -e dev -p proj1 -f proj1-201909270820.tar.gz

	2020-01-07 16:13:13.007 INFO clean up the old version ...
	2020-01-07 16:13:13.007 INFO clean job finished,wget the file ...
	--2020-01-07 16:13:13--  http://119.252.143.91/h5/proj1-201909270820.tar.gz
	正在连接 119.252.143.91:80... 已连接。
	已发出 HTTP 请求，正在等待回应... 200 OK
	长度：2126666 (2.0M) [text/plain]
	正在保存至: “proj1-201909270820.tar.gz”
	
	100%[===============================================================================================================================================================>] 2,126,666   2.37MB/s 用时 0.9s
	
	2020-01-07 16:13:14 (2.37 MB/s) - 已保存 “proj1-201909270820.tar.gz” [2126666/2126666])
	
	2020-01-07 16:13:14.007 INFO wget job finished,extract file ...
	./proj1/
	./proj1/css/
	./proj1/css/account-report.css
	...
	...
	...
	2020-01-07 16:13:15.007 INFO extract job finished ...	  
	
.. note::
	  #. 执行前置任务脚本之前，可以先通过变量获取脚本获取所需部署项目的文件名
	  #. -f 参数表示指定的文件名，文件名一般约定版本命名方式命名。

主任务脚本

.. code-block::	bash

	(skstack) [root@devops pl_deploy_package]# python main_static_deploy.py -e dev -p proj1
	start deploy static files
	 [WARNING]: Found variable using reserved name: hosts
	
	PLAY [svn] **********************************************************************************************************************************************************************************************
	
	TASK [change local dir owner] ***************************************************************************************************************************************************************************
	ok: [svn -> 127.0.0.1]
	
	TASK [sync  to the destination] *************************************************************************************************************************************************************************
	ok: [svn]
	
	PLAY RECAP **********************************************************************************************************************************************************************************************
	svn                        : ok=2    changed=0    unreachable=0    failed=0
	
	(skstack) [root@devops pl_deploy_package]#




.. note::
	  #. 指定目标主机模式：python main_static_deploy.py -e dev -p proj1 -a host1



最佳实践
--------------------------------

步骤概述
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 #. 安装
 #. 配置各环境的json配置文件
 #. 配置nginx版本仓库
 #. 项目变量获取脚本测试
 #. 前置任务、主任务脚本测试
 #. 配置skstack web工单系统将各项目注册到工单系统，以方便用户通过web完成自动化发布流程，配置步骤如下：
 
	 - 注册工单可选变量并校验
	 -  配置变量组管理工单可选变量
	 - 配置工单，关联变量组、主任务运行脚本、和相关运行参数


安装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 #. 不同环境单独使用一台ansible服务器作为作为配置管理服务器；如prod一台ansible， stage一台ansible。
 #. 将skstack_plugins插件库安装到ansible服务器的/opt/soft/目录，并创建/opt/tarsource/目录作为tar.gz项目文件的临时版本库。
 #. skstack web将不同环境的ansible服务器（插件库所在服务器）注册到skstack 工单系统

配置文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	如生产环境代号prod 准生产环境为stage，可以为每个环境单独准备一份配置文件；
	复制demo.json生成两个配置文件：prod_conf.json  stage_conf.json。配置文件必须以_conf.json 结尾，否则插件库中的脚本不会识别
	具体配置参数，参考配置文件说明章节


配置nginx版本仓库
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

定义仓库根目录和相关location如下：

::

   location /tarbase {    #定义tar.gz包仓库根目录
        alias /tarbase ;
        autoindex on ;  #激活autoindex选项，方便发布插件爬虫获取仓库地址下对应项目的文件名
   }
   
	1 在nginx版本仓库根目录"/tarbase"创建对应的项目子目录如proj1，并将对应打包好的文件上传到对应项目子目录里面
	2 配置完成后可以通过浏览器访问http://nginx_host/tarbase/proj1 获取到对应项目所有版本列表，表示配置成功，如下所示：
	
		Index of /tarbase/proj1/
	../
		proj1-v1.4.1-201909101044.tar.gz        10-Sep-2019 02:51             1993603
		proj1-v1.4.2-201909111428.tar.gz        11-Sep-2019 09:45             1997339
		proj1-v1.4.2-201909231641.tar.gz        23-Sep-2019 08:44             2005695

项目变量获取脚本测试
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用项目变量获取脚本检查是否可以获取到指定关键字项目列表，详见命令行模式脚本效果演示章节

任务脚本功能测试
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 #.使用前置任务脚本测试，确保文件可以正常从nginx仓库下载到发布系统本地仓库并解压
 #.使用主任务脚本保证，可以将发布插件本地仓库的文件同步到目标服务器；
 #.使用方法详见命令行模式脚本效果演示章节

.. note::
	  #. 执行主任务脚本之前，需先完成ansible服务器到目标服务器的认证，保证ansible可以管理目标服务器


Skstack Web工单系统配置
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


  
1 注册工单可选变量并校验，需要配置两个可选变量，参数配置如下：

::

	 变量名：proj1Version
	 变量表单标签名字：Version
	描述：此变量相关描述内容
	变量取值方法：脚本生成
	变量表单类型：单选select2下拉框
	变量值：为空（因这里使用脚本生成可选变量，非管理员定义，所以无需定义）
	变量获取脚本：python /opt/soft/skstack_plugins/pl_deploy_package/var_package_version.py -e prod -p proj1
	所属环境：PROD （若无请先添加环境分类）
	所属分类：DeployTar （若无请先添加用途分类）
	

 
2 配置变量组管理工单可选变量

::

	名字：proj1_public
	描述：proj1工单使用的提供给用户的可选变量组
	变量：proj1Version  （关联上述步骤配置的变量）
	所属环境：PROD （若无请先添加环境分类）
	所属分类：DeployTar （若无请先添加用途分类）

 
3 配置工单，关联变量组、主任务运行脚本、和相关运行参数

::

	工单名字：proj1
	项目描述：改工单所发布的项目进行简要描述，方便提单用户通过帮助按钮阅读
	提单权限用户：选择具有提单权限的用户组，需要先到用户管理界面添加相关用户组
	项目环境：PROD
	项目分类：DeployTar
	是否激活工单：激活   #未激活工单，提单用户无法看到
	内置变量：{"ProjName":"proj1"}
	可选参数组：proj1_public
	前置任务：/root/.virtualenvs/skstack/bin/python /opt/soft/skstack_plugins/pl_deploy_package/pre_package_download.py -e dev -p {ProjName} -f "{proj1Version}"
	主任务：/root/.virtualenvs/skstack/bin/python /opt/soft/skstack_plugins/pl_deploy_package/main_static_deploy.py -e dev -p {ProjName}
	后置任务：留空
	是否开启审核：此处不勾选，若需使用审核流程，可参考用户系统，审核流程配置环节
	审核流程：若需使用审核流程，可参考用户系统，审核流程配置环节
	其余选项：暂未上线，不勾选
	配置中心：若skstack_plugins插件库和skstack web平台不在同一台服务器此处需要选择插件库所在的服务器，默认为空表示，插件库和skstack web工单系统共用一个操作系统实例

	 



