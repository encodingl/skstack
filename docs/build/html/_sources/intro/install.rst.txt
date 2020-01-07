安装手册
===============


环境说明
----------------

* Python3.7.4
* Django2.2.5 
* system：windows or linux 
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

请将服务器端安装在centos7上

 #. git clone $GitUrl/skstack.git
 #. yum install ansible -y
 #. yum install smartmontools -y
 #. yum install mysql-devel gcc gcc-devel python-devel
 #. cd skstack 进入到项目主目录
 #. workon skstack 切换到skstack的python虚拟环境
 #. pip install -r requirements.txt


配置文件修改
~~~~~~~~~~~~~~~~~~~~~~

 #. cd skstack
 #. 生产环境：cp skstack_demo.conf skstack_prod.conf;编辑skstack_prod.conf文件填写mysql数据库等信息
 #. 开发环境：cp skstack_demo.conf skstack_dev.conf;编辑skstack_dev.conf文件填写mysql数据库等信息
 
.. note::
	  skstack_dev.conf skstack_prod.conf两个文件同时存在，会优先读取skstack_dev.conf配置文件
..

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

初始化数据：

 #. python manage.py makemigrations
 #. python manage.py migrate
 #. python manage.py createsuperuser  创建用户

运行web平台和登录
~~~~~~~~~~~~~~~~~~~~~~

python manage.py runserver 0.0.0.0:8000

登录页面

.. image:: _images/login.png
   :width: 800
   :height: 450
   :alt: image not found

安装工单系统插件
~~~~~~~~~~~~~~~~~~~~~~

详见各插件安装使用说明文档

