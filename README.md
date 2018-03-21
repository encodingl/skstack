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
#### step0:前置配置 安装python虚拟机.为了不影响其他python应用环境强烈建议安装python虚拟机
virtualenv venv-skipper --python=/usr/local/bin/python

#### step1:准备
请将服务器端安装在centosi6 or 7上
git clone http://gitlab.szyy.com/opergroup/skipper.git<br>
若上调命令不行请使用如下命令克隆代码 git clone git@gitlab.szyy.com:/var/opt/gitlab/git-data/repositories/opergroup/skipper.git<br>
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
# dashboard
<img src="https://github.com/guohongze/skipper/blob/master/static/dist/img/demo.png"></img>
# 安全
建议不要将程序启动在有公网可以直接访问的设备上，如果需要请使用VPN。<br>
建议生产环境中使用https配置服务器<br>



<api接口文档,共8个接口,包含邮件接口,微信接口,电话接口,短信接口,钉钉接口,组接口(只包含前面5种接口),zabbix调用接口,grafana接口>
level级别为:debug,info,warning,error,fatal.
接口使用说明:
1.邮件接口:
请求方url: http://10.8.48.195:8000/skapi/api/sendmail?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'level':'',                                      #指定事件级别
    'subject':'xxxxx',                               #指定邮件标题
    'receiverlist','test1@mljr.com,test2@mljr.com',  #指定邮件收件人,多人邮件已逗号分隔
    'content','xxxxx',                               #指定邮件正文,默认为 text 格式.
}

2.微信接口:
请求方url: http://10.8.48.195:8000/skapi/api/sendweixin?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'level':'',                                      #指定事件级别
    'receiverlist':'test1@mljr.com,test2@mljr.com',  #指定微信接收人,多人以逗号分隔,账号统一用注册的个人企业邮箱.
    'serial','xxxxx',             #指定微信分组编号
    'content','xxxxx',            #指定微信内容.
}

3.短信接口:
请求方url: http://10.8.48.195:8000/skapi/api/sendsms?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'level':'',                       #指定事件级别
    'mobiles':'186216281xxx,123456',  #指定接收人的电话号码,多个号码以逗号分隔
    'content','xxxxx',       #指定接收的内容
}


4.电话接口:
请求方url: http://10.8.48.195:8000/skapi/api/aliyun_voice?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'level':'',         #指定事件级别,如:debug,info,warning,error,fatal.
    'type':'',          #替换阿里云语音播报中的变量${type}. 如果为空, 默认是  "有用分期" ,可选项
    'mobiles':'186216281xxx,123456',  #指定接收人的电话号码,多人以逗号分隔,必选项.
    'content','xxxxx',  #指定事件备注描述,后台日志记录用.
}

5.钉钉接口
   ....

6.组接口:(通过组管里前面5种接口)
请求方url: http://10.8.48.195:8000/skapi/monitor/sendgroup?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    ...
}

7.zabbix接口:
请求方url: http://10.8.48.195:8000/skapi/monitor/zabbixalart?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'subject':'xxx',    #标题
    'content','xxxxx',  #内容
    'type','xxxxx',  #可选,特殊了分组使用
}

8.grafana接口:
请求方url: http://10.8.48.195:8000/skapi/grafana/?token=xxxxxxxx
请求方法: POST
请求数据格式:
{
    'content','xxxxx',  #json格式数据
}









