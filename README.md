# skstack

* skstack主要用于版本发布等devops工作，基于python3、django2.2、AdminLTE开发。
* 文档详见：https://skstack.readthedocs.io/zh_CN/latest/
* 主要功能如下：
	1. 工单系统：发布、多级审核、执行、审计、定时任务、多环境标签管理、工单权限配置、官方配套插件、支持自定义插件
	2. 用户系统：用户、用户组、菜单权限、审核流程配置
	3. 仪表盘：发布统计、工单统计、环境统计等
	4. 系统管理：系统参数配置、ansible hosts索引、定时任务实时监控


# skstack_plugins

* skstack_plugins为skstack项目工单系统官方集成插件，目前主要上线版本发布任务插件，基于python3开发。
* git地址：https://github.com/encodingl/skstack_plugins
* 文档详见：https://skstack.readthedocs.io/zh_CN/latest/plugins/overview.html#
* 主要功能如下：
	1. 基于gitlab仓库版本管理的发布插件
	2. 基于docker镜像仓库版本管理的发布插件
	3. 基于nginx坐版本管理的爬虫方式获取版本进行发布的插件




