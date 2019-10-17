# skstack
The open source operation platform : CMDB, project deploy, DevOps  . <br>
开源DevOps平台：资产管理、项目部署、自动运维、系统监控
# Requirements
#### 服务器
python 3.7<br>
django 2.2<br>
system：windows or linux <br>
Verified operating system：Centos7（suggested ）and  windlows 10<br>



## 服务端说明
#### step_pre:前置配置 安装python虚拟机.为了不影响其他python应用环境强烈建议安装python虚拟机
1 安装python 3.7  略<br>

2 安装对应python版本的pip<br>
wget https://bootstrap.pypa.io/get-pip.py<br>
/python2.7.16_path/bin/python get-pip.py<br>

3 在python2.7.16的pip下安装如下包  该步骤非常重要，请不要用系统自带的pip安装，否则提示找不到virtualenvwrapper<br>
pip install virtualenv<br>
pip install virtualenvwrapper<br>
source /path/virtualenvwrapper.sh<br>

4 创建python虚拟环境<br>
mkvirtualenv skstack<br>
workon skstack<br>


#### step1:准备
请将服务器端安装在centos7上
git clone $GitUrl/skstack.git<br>
yum install ansible -y<br>
yum install smartmontools -y<br>
yum install python python-devel -y<br>
#### step2:数据库
yum install -y mariadb-server mariadb-devel<br>
service mariadb start<br>
chkconfig mariadb on<br>
mysql<br>
CREATE DATABASE skstack DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
#### step3:配置
cd skstack<br>
编辑skstack_prod.conf文件填写mysql数据库信息<br>
如果有skstack_dev.conf文件，会先读取，主要用于开发模式<br>
#### step4:配置免密钥登陆
ssh-keygen (可选)<br>
ssh-copy-id -i /root/.ssh/id_rsa.pub {客户机IP}<br>
ansible和shell管理客户机需要此配置

#### step5:运行
切换到python虚拟机环境<br>
source /home/pythonenv/venv-skstack/bin/activate<br>
再执行如下命令<br>
easy_install pip <br>
pip install -r requirements.txt<br>
python manage.py makemigrations<br>
python manage.py migrate<br>
python manage.py createsuperuser<br>
python manage.py runserver 0.0.0.0:8000


# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>








