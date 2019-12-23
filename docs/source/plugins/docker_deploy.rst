Docker部署插件使用指南
==============================

概述
--------------------------------

docker部署插件支持如下几种执行模式：


- update：版本更新优雅模式，过程如下：

	#. 下载镜像 ；
	#. 从eureka注销服务（未使用eureka则跳过该步骤）；
	#. 等待eureka刷新缓存（未使用eureka则跳过该步骤） ；
	#. 停止服务 ；
	#. 启动新镜像；
	#. eureka健康检测（未使用eureka则跳过该步骤）

- restart：重启服务
  
- inquery：版本查询

- rollback：回滚，回滚到当前项目docker状态为Exit的最新版本；只能回滚一次，若执行多次，会在最新两个版本之间来回变更。

- update_hard：版本更新强制模式，过程如下：

	#. 下载镜像   
	#. 停止服务 
	#. 启动新镜像；hard模式用于常规update模式无法更新或者第一次发布服务的情况。

.. note::
	  #. 部署方式：多个节点情况下为滚动更新；
	  #. docker镜像tag限制：限制使用latest更新；未使用eureka服务的项目update模式过程与update_hard模式一致
..

目录说明
--------------------------------

.. code-block::	bash

	pl_deploy_docker/			#docker部署插件主目录
	├── conf					#配置文件目录
	│   ├── demo.json			#配置文件参考模板
	│   ├── prod_conf.json		#_conf.json结尾的文件为用户定义的线上配置文件
	│   └── stage_conf.json
	├── main_docker_deploy.py	#docker部署插件主任务脚本
	├── sc_docker_rollback.py		
	├── sc_eureka_health_check.sh
	├── sc_restart.yml
	├── sc_rollback.yml
	├── sc_update_hard.yml
	├── sc_update_soft.yml
	└── var_json_keys.py		#如需将多个项目合并到一个工单上面，可以通过该变量获取脚本获取配置文件里面的多个项目名称
	


配置文件说明
--------------------------------

.. code-block:: python

	{
	
		"public": { #所有项目共有配置参数区域
			"EurekaUrl": "http://eureka.demo.com:9001" #eureka地址，若无可以留空
		},
	
		"demo1": {#项目名
			"DockerImageURL": "registry.cn-hongkong.aliyuncs.com/namespace_demo/",  #docker镜像命名空间地址
			"hosts": "demo1",	#指定需要部署到目标主机的ansible hosts group
			"DockerRunArg": " -d -m 1000m -v /data/logs:/logs", #docker run 指定运行参数，可为空
			"DockerRunCmd": "",  #指定docker起来后运行的命令，覆盖docker file构建时的默认命令，可为空
			"AppSpringName": "null"  #指定该项目注册在eureka中的生产者名称，若未使用eureka，可以指定为null
		},
	
		"demo2": {
			"DockerImageURL": "registry.cn-hongkong.aliyuncs.com/namespace_demo/",
			"hosts": "none",
			"DockerRunArg": "",
			"DockerRunCmd": "java  -jar -Xms2g -Xmx4g demo2.jar --spring.config.location=file:./config/demo2.yml",
			"AppSpringName": "demo2"
		}
	}


.. note::
	  #. DockerImageURL：使用插件之前需要用户先自己完成服务器到镜像仓库认证，插件不负责认证;镜像地址拼接方式为DockerImageURL+"项目名字"+":latest"
	  #. hosts：，若显示指定为none，这插件会读取插件所在服务器的ansible hosts文件中group等于项目名的目标主机，若无则报错
	  #. public key为配置文件内置参数，用于指定EurekaUrl和后期需要扩展的其他公共参数，项目名不可使用该key命名
..

脚本说明
--------------------------------

变量获取脚本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::	bash

	(skstack) [root@host175 pl_deploy_docker]# python var_json_keys.py -h
	usage: var_json_keys.py [-h] [-k [keyword1|keyword2]] [-e [prod|stage|dev]]
	
	version 2.0.0
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -k [keyword1|keyword2], --filter-keyword [keyword1|keyword2]
	                        the project keyword you want to filter
	  -e [prod|stage|dev], --environment [prod|stage|dev]
	                        the environment you need deploy

主任务脚本
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block::	bash

	(skstack) [root@registry pl_deploy_docker]# python main_docker_deploy.py -h
	usage: main_docker_deploy.py [-h] [-e [prod|stage|dev...]]
	                             [-p [proj01|proj02|...]] [-t [v0.1.0|latest|...]]
	                             [-a [192.168.1.22|AnsbileHostsName|...]]
	                             [-w [3s|1m|...]]
	                             [-m [update|restart|inquiry|rollback|update_hard]]
	
	version 2.0.0
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -e [prod|stage|dev...], --Environment [prod|stage|dev...]
	                        input the environment in which the script needs to be
	                        executed
	  -p [proj01|proj02|...], --proj-docker [proj01|proj02|...]
	                        the docker project you want to depoly
	  -t [v0.1.0|latest|...], --DockerImageTag [v0.1.0|latest|...]
	                        input the docker image tag default=latest
	  -a [192.168.1.22|AnsbileHostsName|...], --AnsibleHosts [192.168.1.22|AnsbileHostsName|...]
	                        input AnsibleHosts,default is the same as -p parameter
	  -w [3s|1m|...], --WaitTimes [3s|1m|...]
	                        input securyty wait times for rolling update
	                        default=60s
	  -m [update|restart|inquiry|rollback|update_hard], --ExecMode [update|restart|inquiry|rollback|update_hard]
	                        input the execution mode you need
	(skstack) [root@registry pl_deploy_docker]#

最佳实践
--------------------------------


配置文件
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Web模式效果演示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

提单页面如下：

.. image:: _images/docker_submit.png
   :alt: image not found

.. note::
	  #. Project项下来菜单表示为该工单可选的docker项目，通过插件变量获取脚本从配置文件获取指定项目；
	  #. 多个docker项目可以合并到一个工单上，也可以一个docker项目使用一个工单

结果页展示：

.. image:: _images/docker_update_result.png
   :alt: image not found
   
.. note::
	  #. 结果页面，参考ansible结果日志


 

命令行模式效果演示
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






