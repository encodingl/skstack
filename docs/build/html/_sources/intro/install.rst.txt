安装手册
===============


环境说明
----------------

* Python3.7.4
* Django2.2.5 
* system：linux、macos、windows
* 生产环境建议：Centos7或以上版本（suggested ）

 

安装步骤
-------------

安装python虚拟机 
~~~~~~~~~~~~~~~~~~~~~~

 * 安装python 3.7和python虚拟机  略（为了不影响其他python应用环境强烈建议安装python虚拟机）；
 * 用virtualenvwrapper按照python虚拟环境
 * 安装位置建议：/root/.virtualenvs/skstack
  
  #. mkvirtualenv skstack
  #. workon skstack



安装源码和依赖包
~~~~~~~~~~~~~~~~~~~~~~

项目地址：https://github.com/encodingl/skstack

请将服务器端安装在centos7或以上版本

 #. git clone git@github.com:encodingl/skstack.git
 #. yum install ansible -y
 #. yum install smartmontools -y
 #. yum install mysql-devel gcc gcc-devel python-devel
 #. cd skstack 进入到项目主目录
 #. workon skstack 切换到skstack的python虚拟环境
 #. pip install -r requirements.txt




建库和初始化数据
~~~~~~~~~~~~~~~~~~~~~~

安装数据库

 #. yum install -y mariadb-server mariadb-devel
 #. service mariadb start
 #. chkconfig mariadb on

创建建库和数据库用户

 #. mysql -uroot -p登录数据库
 #. CREATE DATABASE skstack DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;  创建schema
 #. GRANT ALL PRIVILEGES ON skstack.* TO 'ser_skstack'@'localhost' IDENTIFIED BY 'Password59584'; 创建用户
 #. flush privileges;


 #. workon skstack 切换到python虚拟机环境

安装redis
~~~~~~~~~~~~~~~~~~~~~~

 #. yum install redis
 #. systemctl start redis

.. note::
	  定时任务和任务锁需要使用到redis功能
..

配置文件修改
~~~~~~~~~~~~~~~~~~~~~~

 #. cd skstack
 #. 生产环境：cp skstack_demo.conf skstack_prod.conf;编辑skstack_prod.conf文件填写mysql、redis等信息
 #. 开发环境：cp skstack_demo.conf skstack_dev.conf;编辑skstack_dev.conf文件填写mysql、redis等信息
 
配置文件说明 
::

	 [db]   #数据库配置信息
	engine = mysql
	host = localhost
	port = 3306
	user = ser_skstack
	password = IacjV+HJpQcskqaW1
	database = skstack
	
	[redis]  #redis配置信息，任务锁功能使用
	host = localhost
	port = 6389
	db = 7
	password =
	
	[log]  #日志路径和级别配置
	log_path = /opt/sklogs/skstack/
	log_level = info
	
	[setup]
	debug = False  # 是否打开debug模式，建议生产环境设置False，开发者环境使用True
	allowed_hosts = *  #允许访问web的客户端主机
	
	[config]
	ansible_path = /etc/ansible/  #ansible配置主目录

	[celery] #celery任务配置项 用于定时任务
	celery_broker_url = redis://localhost:6389/5  #celery使用redis，可以和任务锁使用同一个redis实例的不同db
	
	[flower] #celery flower外链地址，后续release版本将整合到[celery]下
	flower_url = http://ip:5555/dashboard


.. note::
	  skstack_dev.conf skstack_prod.conf两个文件同时存在，会优先读取skstack_dev.conf配置文件
..

初始化数据：

 #. python manage.py makemigrations
 #. python manage.py migrate
 #. python manage.py createsuperuser  创建用户

运行web平台和登录
~~~~~~~~~~~~~~~~~~~~~~

 #. workon skstack #切换python虚拟机环境
 #. ./start_web.sh #启动web
 #. ./start_celery.sh #启动celery相关任务 ，若不使用定时任务功能，该脚本不需要执行


登录页面

.. image:: _images/login.png
   :width: 800
   :height: 450
   :alt: image not found

停止web平台
~~~~~~~~~~~~~~~~~~~~~~

 #. ./stop_web.sh #停止web
 #. ./stop_celery.sh #停止celery相关任务 
 
安装工单系统插件
~~~~~~~~~~~~~~~~~~~~~~

详见各插件安装使用说明文档

