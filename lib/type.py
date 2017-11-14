#coding:utf8


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
    (0,'---------'),
    (1,'运维'),
    (2,'开发'),
    (3,'测试'),
    (4,'产品'),
    (5,'其他')
)

Alarm_TYPE = (
    (0, u'微信'),
    (1, u'邮件'),
    (2, u'短信'),
    (3, u'电话'),
    (4, u'钉钉'),
)