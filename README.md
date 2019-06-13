# skipper
The open source operation platform : CMDB, project deploy, DevOps  . <br>
开源DevOps平台：资产管理、项目部署、自动运维、系统监控
# Requirements
#### 服务器
python 2.7<br>
django 1.9.8<br>
sh 1.12.9<br>
mysql-python 1.2.5<br>
ansible 2.0+<br>
#### 客户端
python 2.6+<br>
smartmontools<br>


## 服务端说明
#### step_pre:前置配置 安装python虚拟机.为了不影响其他python应用环境强烈建议安装python虚拟机
1 安装python 2.7.16  略

2 安装对应python版本的pip
wget https://bootstrap.pypa.io/get-pip.py<br>
/python2.7.16_path/bin/python get-pip.py<br>

3 在python2.7.16的pip下安装如下包  该步骤非常重要，请不要用系统自带的pip安装，否则提示找不到virtualenvwrapper
pip install virtualenv<br>
pip install virtualenvwrapper<br>
source /path/virtualenvwrapper.sh<br>

4 创建python虚拟环境
mkvirtualenv skipper<br>
workon skipper<br>


#### step1:准备
请将服务器端安装在centosi6 or 7上
git clone git@github.com:encodingl/skipper.git<br>
yum install ansible -y<br>
yum install smartmontools -y<br>
yum install python python-devel -y<br>
#### step2:数据库
yum install -y mariadb-server mariadb-devel<br>
service mariadb start<br>
chkconfig mariadb on<br>
mysql<br>
CREATE DATABASE skipper DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
#### step3:配置
cd skipper<br>
编辑skipper.conf文件填写mysql数据库信息
#### step4:配置免密钥登陆客机
ssh-keygen (可选)<br>
ssh-copy-id -i /root/.ssh/id_rsa.pub {客户机IP}<br>
ansible和shell管理客户机需要此配置

#### step5:运行
切换到python虚拟机环境<br>
source /home/pythonenv/venv-skipper/bin/activate<br>
再执行如下命令<br>
easy_install pip <br>
pip install -r requirements.txt<br>
python manage.py makemigrations<br>
python manage.py migrate<br>
python manage.py createsuperuser<br>
python manage.py runserver 0.0.0.0:8000
## 客户端说明
说明：为保证注册IP是管理IP（后续会被ansible等调用），客户端的IP抓取目前使用主机名解析，也就是说主机名必须可以被解析才能执行自动上报脚本，否则报错。
如：主机名为centos6 请在/etc/hosts中加入相应的解析 192.168.x.x centos6，这样再执行agent_post_info.py 可以保证正常运行。
centos7不进行解析也可获取主机IP，但是centos6必须在/etc/hosts对主机名进行解析。
#### step1:
yum install -y smartmontools <br>
yum install -y dmidecode
#### step2:
在客户机上执行 scripts/agent_post_info.py 文件自动上报主机信息<br>
注意：编写前请编辑scripts/agent_post_info.py文件 保证 token 和server_url是正确的

## 访问
http://your_server_ip:8000<br>
使用自己createsuperuser创建的用户名密码

# API
#### 获取主机信息
http://your_server_ip:8000/cmdb/get/host/?token=your_token&name=host_name <br>
#### 获取组信息
http://your_server_ip:8000/cmdb/get/group/?token=your_token&name=group_name <br>
http://your_server_ip:8000/cmdb/get/group/?token=your_token&name=all <br>

# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>








