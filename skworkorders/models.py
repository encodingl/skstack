#! /usr/bin/env python
# -*- coding: utf-8 -*-

#x6



from django.db import models
from skaccounts.models import UserGroup,AuditFlow


# Create your models here.3




WorkOrder_STATUS = (
    (str("no"), "停用"),
    (str("yes"), "激活"),
    )

WorkOrder_SOURCE = (
    (str("skstack"), "skstack"),
    (str("local"), "local"),
    )

WorkOrder_REPO_MODE = (
    (str("tag"), "tag"),
    (str("branch"), "branch"),
    (str("other"), "other"),
    )
WorkOrder_REPO_TYPE = (
    (str("git"), "git"),
    (str("other"), "other"),
    )



WorkOrderFlow_STATUS = (
    (str(0), "新建提交"),
    (str(1), "l1审核通过"),
    (str(2), "l1审核拒绝"),
    (str(3), "执行成功"),
    (str(4), "执行失败"),
    (str(5), "l2审核通过"),
    (str(6), "l2审核拒绝"),
    (str(7), "l3审核通过"),
    (str(8), "l3审核拒绝"),
    (str(9), "撤销"),
    (str("PENDING"), "后台执行"),
    (str("REVOKED"), "计划撤销"),
    )



WorkOrder_AUDIT_ENABLE = (
    (str("no"), "关闭"),
    (str("yes"), "开启"),
    )

VARS_METHOD = (
    (str("script"), "脚本生成"),
    (str("admin_def"), "管理员定义"),
    (str("manual"), "用户输入"),
    )

VARS_FORM_TYPE = (
    (str("Select"), "单选select2下拉框"),
    (str("RadioSelect"), "单选icheck Radio"),
    (str("SelectMultiple"), "复选select2下拉框"),
    (str("CheckboxSelectMultiple"), "复选icheck box"),
    (str("TextInput"), "单行用户输入"),
    (str("Textarea"), "多行用户输入"),
    )
# Create your models here.

class ConfigCenter(models.Model):
    name  = models.CharField("名称",max_length=50)
    ip = models.GenericIPAddressField("ip",max_length=50)
    username  = models.CharField("用户名",max_length=50, default="root")
    password  = models.CharField("密码",max_length=50, null=True, blank=True)
    port  = models.PositiveIntegerField("ssh port", default=22)
    rsa_key  = models.CharField("rsa key",max_length=50, null=True, blank=True)
    desc = models.CharField("描述", max_length=300, null=True, blank=True)
    def __str__(self):
        return self.name    
    
class Environment(models.Model):
    name_english  = models.CharField("英文简称",max_length=50,unique=True)
    label_sort = models.PositiveIntegerField("label_sort",default=10)
    desc = models.CharField("描述", max_length=300, null=True, blank=True)
    
    def __str__(self):
        return self.name_english
    
class WorkOrderGroup(models.Model):
    name = models.CharField(max_length=100,unique=True)    # permission = models.ManyToManyField(PermissionList, null=True, blank=True)
    desc = models.CharField("描述", max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Vars(models.Model): 
    name = models.CharField("变量名",max_length=50,unique=True)
    label_name = models.CharField("变量表单标签名",max_length=50)
    desc  = models.CharField("描述",max_length=100,blank=True)
    value_method = models.CharField("变量取值方法", choices=VARS_METHOD, max_length=50)
    value_form_type = models.CharField("变量表单类型", choices=VARS_FORM_TYPE, max_length=50)
    value_optional  = models.CharField("变量值",max_length=300,blank=True)  
    value_script  = models.CharField("变量获取脚本",max_length=200,null=True,blank=True)
    env = models.ForeignKey(Environment, verbose_name="所属环境", on_delete=models.PROTECT, null=True, blank=True) 
    group = models.ForeignKey(WorkOrderGroup, verbose_name="所属分类", on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.name
    
class VarsGroup(models.Model): 
    name = models.CharField("名字",max_length=50,unique=True)
    desc  = models.CharField("描述",max_length=300)
    vars = models.ManyToManyField(Vars, verbose_name="变量",blank=True)
    env = models.ForeignKey(Environment, verbose_name="所属环境", on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey(WorkOrderGroup, verbose_name="所属分类", on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.name
    
    
class WorkOrder(models.Model):   
    name = models.CharField("工单名字",max_length=100)
    desc  = models.CharField("项目描述",max_length=300)  
    user_dep = models.ManyToManyField(UserGroup, verbose_name="提单权限用户",blank=True)
    env = models.ForeignKey(Environment, verbose_name="项目环境", on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey(WorkOrderGroup, verbose_name="所属分类", on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField("是否激活工单", choices=WorkOrder_STATUS, max_length=10,default="no")
    
    var_built_in = models.CharField("内置变量",max_length=300,blank=True)
    var_opional_switch = models.BooleanField("是否开启用户可选参数")
    var_opional = models.ForeignKey(VarsGroup, verbose_name="可选参数组", on_delete=models.PROTECT, null=True, blank=True)
    
    pre_task = models.CharField("前置任务",max_length=500,null=True, blank=True)
    main_task = models.CharField("主任务",max_length=500,null=True, blank=True)
    post_task = models.CharField("后置任务",max_length=500,null=True, blank=True)
   
    audit_enable = models.BooleanField("是否开启审核")
    audit_flow = models.ForeignKey(AuditFlow, verbose_name="审核流程", on_delete=models.PROTECT, null=True,blank=True)
    
    
    schedule_enable = models.BooleanField("是否开启定时任务",default=False)
    back_exe_enable = models.BooleanField("是否开启后台执行选择按钮",default=False)
    auto_exe_enable = models.BooleanField("是否开启批准后自动执行选择按钮",default=False)
    task_lock_enable = models.BooleanField("是否开启任务锁",default=False)
    
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True,null=True)
    updated_at = models.DateTimeField('修改时间', auto_now_add=True,null=True)
    template_enable = models.BooleanField("是否转为模板")    
    config_center = models.ForeignKey(ConfigCenter, verbose_name="配置中心", on_delete=models.PROTECT, null=True,blank=True)
    def __str__(self):
        return self.name
    
class WorkOrderFlow(models.Model):
    title = models.CharField("标题",max_length=50)
    desc  = models.CharField("说明",max_length=300,null=True,blank=True)
    user_commit = models.CharField("申请人",max_length=50,null=True,blank=True)
    workorder = models.CharField("工单名称",max_length=50,null=True,blank=True)
    workorder_group = models.CharField("工单分类",max_length=50,null=True,blank=True)
    workorder_id = models.CharField("项目id",max_length=50,null=True,blank=True)
    env = models.CharField("环境",max_length=50,null=True,blank=True)
    status = models.CharField("状态", choices=WorkOrderFlow_STATUS, max_length=30, null=True, blank=True)
    user_vars = models.CharField("选定参数",max_length=300,null=True,blank=True)
    created_at = models.DateTimeField('提单时间', auto_now_add=True,null=True)
    audit_level = models.CharField("审核层级",max_length=50,null=True,blank=True)
    user_l1 = models.CharField("l1审核用户",max_length=50,null=True,blank=True)
    comment_l1 = models.CharField("l1审核意见",max_length=100,null=True,blank=True)
    updated_at_l1 = models.DateTimeField('l1审核时间', null=True)
    user_l2 = models.CharField("l2审核用户",max_length=50,null=True,blank=True)
    comment_l2 = models.CharField("l2审核意见",max_length=100,null=True,blank=True)
    updated_at_l2 = models.DateTimeField('l2审核时间', null=True)
    user_l3 = models.CharField("l3审核用户",max_length=50,null=True,blank=True)
    comment_l3 = models.CharField("l3审核意见",max_length=100,null=True,blank=True)
    updated_at_l3 = models.DateTimeField('l3审核时间', null=True)
    finished_at = models.DateTimeField('完成时间',null=True)
    celery_task_id = models.CharField("后台任务id",max_length=50,null=True,blank=True)
    celery_schedule_time = models.DateTimeField('计划执行时间',null=True,blank=True)
    back_exe_enable = models.BooleanField("是否开启后台执行",default=False)
    auto_exe_enable = models.BooleanField("是否开启批准后自动执行",default=False)
    def __str__(self):
        return self.title
    
