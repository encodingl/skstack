# coding:utf8


ASSET_TYPE = (
    (1, u"物理机"),
    (2, u"虚拟机"),
    (3, u"交换机"),
    (4, u"路由器"),
    (5, u"防火墙"),
    (6, u"Docker"),
    (7, u"其他")
)

ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
)

MAP_TYPE = (
    (str(1), u"外网"),
    (str(2), u"内网"),
)

AuditFlow_LEVEL = (
    (str(1), u"一层审核"),
    (str(2), u"二层审核"),
    (str(3), u"三层审核"),
)

User_TYPE = (
    (0, '---------'),
    (1, u'应用运维'),
    (2, u'系统运维'),
    (3, u'基础运维'),
    (4, u'dba运维'),
    (5, u'IT支持'),
    (6, u'开发'),
    (7, u'测试'),
    (8, u'产品'),
    (9, u'其他'),
)

Alarm_TYPE = (
    (0, u'邮件'),
    (1, u'短信'),
    (2, u'微信'),
    (3, u'钉钉'),
    (4, u'电话'),
)

WeiXin_Type = (
    (11, u'中间件'),
    (32, u'生产ERROR日志'),
    (22, u'测试用途'),
    (21, u'数据组'),
    (0, u'无')

)

Alarm_TYPE_Code = ['mobile', 'dingding', 'email', 'weixin', 'sms']
Log_Type = ['info', 'warn', 'error', 'fatal']
