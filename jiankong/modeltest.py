from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
class Jk_User(models.Model):
    '''
        用户信息
        标识	id
        用户名	name
        用户名密码	Pwd
        描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    Pwd = models.CharField(max_length=128, null=False)
    DESC = models.CharField(max_length=128, null=True)


class JK_Shebei_Group(models.Model):
    '''
    设备组表
    标识	id
    组名称	Group_Name
    组标记	GroupId
    管理人	UserId
    描述	DESC
    服务端标识	Zabbix_id
    '''
    Group_Name = models.CharField(max_length=64, null=False)
    UserId = models.ForeignKey(Jk_User, null=True)
    GroupId = models.IntegerField(null=True)
    Zabbix_id = models.IntegerField(null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Device_Type(models.Model):
    '''
        设备类型表
        设备类型名称：Server：服务器（物理机/宿主机/云主机/存储）
                      Switches:网络设备（交换机/负载均衡/防火墙/路由器）
        描述
    '''
    TypeName = models.CharField(max_length=16, null=False)
    TypeDESC = models.CharField(max_length=64, null=True)


class Jk_App_lev(models.Model):
    '''
        应用级别表
        级别名称	App_lev_Name
        描述	Desc
    '''
    AppLevName = models.CharField(max_length=32, null=False)
    Desc = models.CharField(max_length=64, null=True)


class Jk_App(models.Model):
    '''
        应用表
        应用名称	AppName
        应用级别	AppLevId
        应用管理部门	App_Me_Dm
        应用维护部门	App_Mt_Dm
        园区	Data_yard
        应用管理人	App_admin
        应用维护人	App_person
        描述	AppDesc
    '''
    AppName = models.CharField(max_length=32, null=False)
    AppLevId = models.ForeignKey(Jk_App_lev)
    App_Me_Dm = models.CharField(max_length=64, null=True)
    App_Mt_Dm = models.CharField(max_length=64, null=True)
    Data_yard = models.CharField(max_length=64, null=True)
    App_admin = models.CharField(max_length=64, null=True)
    App_person = models.CharField(max_length=64, null=True)
    AppDesc = models.CharField(max_length=64, null=True)


class Jk_Switches(models.Model):
    '''
        交换机
        zabbix的hostid       Hostid
        交换机名称	SwitchesName
        Ip地址	ip
        所属设备组	Group
        所属用户	UserId
        备注	DESC
        SNMP状态	Status
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=64, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Status = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Storage(models.Model):
    '''
        存储设备表
        存储名称	StorageName
        Ip地址	ip
        所属组	Group
        所属用户	UserId
        备注	DESC
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=32, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Agent = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fz(models.Model):
    '''
   标识	Fz_id
	    Hostid
    负载均衡名称	Fz_name
    Ip地址	Ip
    所属设备组	Group
    所属用户	UserId
    备注	DESC
    SNMP状态	Status
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=64, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Status = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Resource_Host(models.Model):
    '''
    宿主机ID	Resource_Id
	            Hostid
    主机名	Resource_Name
    主机IP	Ip
    所属设备组	Group
    所属用户	UserId
    描述	DESC
    Agent状态	Agent
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=32, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Agent = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Cloud_Device(models.Model):
    '''
    云主机表
    云主机名称	 Name
    所属用户	UserId
    主机IP	Ip
    所属组	Group
    Agent状态	Agent
    描述	DESC
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=32, null=False)
    UserId = models.ForeignKey(Jk_User, null=True)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    Agent = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Device_Lev(models.Model):
    '''
        设备型号表
        设备型号名称	DeviceLevName
        描述	DeviceLevDesc
    '''
    DeviceLevName = models.CharField(max_length=32, null=False)
    DeviceLevDesc = models.CharField(max_length=64, null=True)


class Jk_Routing(models.Model):
    '''
        路由器
       标识	Routing_Id
	        Hostid
        路由器名称	Name
        Ip地址	Ip
        所属设备组	Group
        所属应用	Application
        所属用户	UserId
        备注	DESC
        SNMP状态	Status
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=64, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Status = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Server(models.Model):
    '''
        物理机表
                     Hostid
        物理机名称	ServerName
        厂商	Vendor
        设备型号	DeviceLev
        设备IP	     IP
        设备数量	Num
        所属设备组	Group
        所属应用	Application_id
        所属用户	User_id
        描述	DESC
        Agent状态	Agent
    '''
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=16, null=False)
    Vendor = models.IntegerField(null=True)
    DeviceLev = models.ForeignKey(Jk_Device_Lev, null=True)
    Ip = models.CharField(max_length=64, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Agent = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fw(models.Model):
    '''
    防火墙
    标识	Fw_id
	        Hostid
    负载均衡名称	Name
    Ip地址	Ip
    所属设备组	Group
    所属用户	UserId
    备注	DESC
    SNMP状态	Status
    '''
    Fw_id = models.AutoField(primary_key=True)
    Hostid = models.IntegerField()
    Name = models.CharField(max_length=64, null=False)
    Ip = models.CharField(max_length=32, null=True)
    Group = models.ForeignKey(JK_Shebei_Group, null=True)
    UserId = models.ForeignKey(Jk_User, null=True)
    Status = models.CharField(max_length=20, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_alert_lev(models.Model):
    '''
        告警级别表
        级别名称	LevName
        描述	DESC
    '''
    LevName = models.CharField(max_length=16, null=False)
    DESC = models.CharField(max_length=64, null=True)


class Jk_Fault(models.Model):
    '''
        故障等级	FaultName
        描述	DESC
    '''
    FaultName = models.CharField(max_length=64, null=False)
    DESC = models.CharField(max_length=64, null=True)


class Jk_alert(models.Model):
    '''
        告警信息表
        告警信息ID	AlertLev
        告警级别	Alert_lev_id
        所属应用	Application
        所属设备	Type_id
        事件Id      Eventid
        zabbix_id   Zabbix_id
        IP	        Ip
        告警内容	message
        发生时间	Oc_time
        受理时间	A_time
        通告人	    Sendto
        受理结果 	Status
        描述	    DESC
    '''
    AlertLev = models.ForeignKey(Jk_alert_lev, max_length=8, null=False)
    Item = models.CharField(max_length=128, null=True)
    Eventid = models.CharField(max_length=20, null=True)
    Zabbix_id = models.IntegerField()
    Ip = models.CharField(max_length=20, null=False)
    Message = models.TextField(null=True)
    Oc_time = models.IntegerField(null=False)
    A_time = models.IntegerField(null=True)
    Sendto = models.CharField(max_length=64, null=True)
    Status = models.IntegerField(null=True)
    DESC = models.CharField(max_length=64, null=True)


class Jk_Alert_His(models.Model):
    '''
    告警信息历史表
    告警信息ID	Alert_His_id
    告警级别	Alert_lev_id
    所属应用	Application_id
    所属设备	Type
    IP          ip
    告警内容	message
    发生时间	Oc_time
    结束时间	End_time
    受理时间	A_time
    通告人	Sendto
    受理结果 	Status
    处理人	Deal_Person
    处理详情	Deal_Details
    处理完成时间	Deal_End_time
    描述	DESC
    '''
    AlertLev = models.ForeignKey(Jk_alert_lev, max_length=8, null=False)
    Type = models.CharField(max_length=32, null=True)
    Eventid = models.CharField(max_length=20, null=True)
    Zabbix_id = models.IntegerField()
    Typename = models.CharField(max_length=128, null=True)
    Item = models.CharField(max_length=128, null=True)
    Ip = models.CharField(max_length=20, null=False)
    Message = models.TextField(null=False)
    Oc_time = models.IntegerField(null=False)
    End_time = models.IntegerField(null=False)
    A_time = models.IntegerField(null=True)
    Sendto = models.CharField(max_length=64, null=False)
    Status = models.IntegerField(null=True)
    Deal_Person = models.CharField(max_length=64, null=True)
    Deal_Details = models.TextField(null=True)
    Deal_End_time = models.IntegerField(null=True)
    DESC = models.CharField(max_length=64, null=True)


class Jk_Fcpu_Pf_Ids(models.Model):
    '''
        物理机CPU监控表
        标识	Id
        CPU监控项	Name
        设备名称	ServerId
        时间戳	Clock
        数值	Value
         描述	DESC
    '''
    Name = models.CharField(max_length=64, null=False)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=512, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Ycpu_Pf_Ids(models.Model):
    '''
        云主机CPU监控表
        Id	int（64）
        Name	Varchar(64)
        Cloud _Id	int（8）
        Clock	Varchar(64)
        数值     Value
        DESC	Varchar(128)
    '''
    Name = models.CharField(max_length=64, null=False)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=512, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Scpu_Pf_Ids(models.Model):
    '''
    宿主机CPU监控表
    Id	int（64）
    Name	Varchar(64)
    Resource_Id	int（8）
    Clock	Varchar(64)
    数值      Value
    DESC	Varchar(128)
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=64, null=False)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=512, null=True)
    DESC = models.CharField(max_length=128, null=True)

class Jk_Jcpu_Pf_Ids(models.Model):
    '''
        交换机CPU监控表
        标识	Id
        CPU监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        数值     Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=64, null=False)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Lcpu_Pf_Ids(models.Model):
    '''
        路由器CPU监控表
        标识	Id
        CPU监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
        数值   Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fzcpu_Pf_Ids(models.Model):
    '''
        负载均衡CPU监控表
        标识	Id
        CPU监控项	Name
        设备名称	Fz_id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fwcpu_Pf_Ids(models.Model):
    '''
        防火墙CPU监控表
        标识	Id
        防火墙监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        数值     Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fmem_Pf_Ids(models.Model):
    '''
        物理机内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Server_Id
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Ymem_Pf_Ids(models.Model):
    '''
        云主机内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Cloud _Id
        时间戳	Clock
        数值    Value
        描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Smem_Pf_Ids(models.Model):
    '''
        宿主机内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Resource_Id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Jmem_Pf_Ids(models.Model):
    '''
        交换机内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Lmem_Pf_Ids(models.Model):
    '''
        路由器内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
        数值  Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fzmem_Pf_Ids(models.Model):
    '''
        负载均衡内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Fz_id
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fwmem_Pf_Ids(models.Model):
    '''
        防火墙内存监控表
        标识	Id
        内存监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        数值     Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Fdisk_Pf_Ids(models.Model):
    '''
        物理机磁盘监控表
        标识	Id
        磁盘监控项	Name
        设备名称	Server_Id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Sdisk_Pf_Ids(models.Model):
    '''
        宿主机磁盘监控表
        标识	Id
        文件系统监控项	Name
        设备名称	Resource_Id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=64, null=True)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Ydisk_Pf_Ids(models.Model):
    '''
        云主机磁盘监控表
        标识	Id
        文件系统监控项	Name
        设备名称	CLoud_Id
        时间戳	Clock
        数值    Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=1024, null=True)
    DESC = models.CharField(max_length=128, null=True)




class Jk_Jdl_Pf_Ids(models.Model):
    '''
        交换机时延监控表
        标识	Id
        时延监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        数值	Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ldl_Pf_Ids(models.Model):
    '''
        路由器时延监控表
        标识	Id
        时延监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
        数值	Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzconn_Pf_Ids(models.Model):
    '''
    负载均衡实连接监控表
    标识	Id
    实连接监控项	Name
    设备名称	Fz_id
    时间戳	Clock
    数值	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzxconn_Pf_Ids(models.Model):
    '''
    负载均衡虚连接数监控表
    标识	Id
    虚连接数监控项	Name
    设备名称	Fz_id
    时间戳	Clock
    数值	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jping_Pf_Ids(models.Model):
    '''
    交换机ping监控表
    标识	Id
    ping监控项	Name
    设备名称	Switches_Id
    时间戳	Clock
    状态	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Lping_Pf_Ids(models.Model):
    '''
    路由器ping监控表
    标识	Id
    CPU监控项	Name
    设备名称	Routing_Id
    时间戳	Clock
    状态	Value
    描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzping_Pf_Ids(models.Model):
    '''
    负载均衡ping监控表
    标识	Id
    ping监控项	Name
    设备名称	Fz_id
    时间戳	Clock
    状态	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fwping_Pf_Ids(models.Model):
    '''
        防火墙ping监控表
        标识	Id
        防火墙连通监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        状态	Value
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jnet_Pf_Ids(models.Model):
    '''
    交换机带宽利用率监控表
   标识	Id
    带宽利用率监控项	Name
    设备名称	Switches_Id
    时间戳	Clock
    数值	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Lnet_Pf_Ids(models.Model):
    '''
    路由器带宽利用率监控表
      标识	Id
    带宽利用率监控项	Name
    设备名称	Routing_Id
    时间戳	Clock
    数值	Value
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_FwSes_Pf_Ids(models.Model):
    '''
    防火墙会话数监控表
   标识	Id
    会话数监控项	Name
    设备名称	Fw_id
    时间戳	Clock
    数值	Value
    描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Value = models.CharField(max_length=20, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fcpu(models.Model):
    '''
    物理机CPU均值表
    标识	Id
    CPU监控项	Name
    设备名称	Server_Id
    时间戳	Clock
    CPU最小值	Min_Cpu
    CPU平均值	AVG_Cpu
    CPU最大值	Max_Cpu
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ycpu(models.Model):
    '''
    云主机CPU均值表
    标识	Id
    CPU监控项	Name
    设备名称	Cloud _Id
    时间戳	Clock
    CPU最小值	Min_Cpu
    CPU平均值	AVG_Cpu
    CPU最大值	Max_Cpu
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Scpu(models.Model):
    '''
        宿主机CPU均值表
        标识	Id
        CPU监控项	Name
        设备名称	Resource_Id
        时间戳	Clock
        CPU最小值	Min_Cpu
        CPU平均值	AVG_Cpu
        CPU最大值	Max_Cpu
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jcpu(models.Model):
    '''
        交换机CPU趋势表
        标识	Id
        CPU监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        CPU最小值	Min_Cpu
        CPU平均值	AVG_Cpu
        CPU最大值	Max_Cpu
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Lcpu(models.Model):
    '''
    路由器CPU趋势表
    标识	Id
    CPU监控项	Name
    设备名称	Routing_Id
    时间戳	Clock
    CPU最小值	Min_Cpu
    CPU平均值	AVG_Cpu
    CPU最大值	Max_Cpu
     描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzcpu(models.Model):
    '''
        负载均衡CPU趋势表
        标识	Id
        CPU监控项	Name
        设备名称	Fz_id
        时间戳	Clock
        CPU最小值	Min_Cpu
        CPU平均值	AVG_Cpu
        CPU最大值	Max_Cpu
         描述	DESC
    '''
    Id = models.AutoField(primary_key=True)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fwcpu(models.Model):
    '''
        防火墙CPU趋势表
        标识	Id
        防火墙监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        CPU最小值	Min_Cpu
        CPU平均值	AVG_Cpu
        CPU最大值	Max_Cpu
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fmem(models.Model):
    '''
        物理机内存趋势表
        标识	Id
        内存监控项	Name
        设备名称	Server_Id
        时间戳	Clock
        内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ymem(models.Model):
    '''
        云主机内存均值表
        标识	Id
        内存监控项	Name
        设备名称	Cloud _Id
        时间戳	Clock
        内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    Id = models.AutoField(primary_key=True)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Smem(models.Model):
    '''
        宿主机内存均值表
        标识	Id
        内存监控项	Name
        设备名称	Resource_Id
        时间戳	Clock
          内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jmem(models.Model):
    '''
        交换机内存趋势表
        标识	Id
        内存监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Lmem(models.Model):
    '''
        路由器内存趋势表
        标识	Id
        内存监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
         内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzmem(models.Model):
    '''
        负载均衡内存趋势表
        标识	Id
        内存监控项	Name
        设备名称	Fz_id
        时间戳	Clock
          内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fwmem(models.Model):
    '''
        防火墙内存趋势表
        标识	Id
        内存监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        内存最小值	Min_Mem
        内存平均值	AVG_Mem
        内存最大值	Max_Mem
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    FwId = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fdisk(models.Model):
    '''
        物理机磁盘趋势表
        标识	Id
        磁盘监控项	Name
        设备名称	Server_Id
        时间戳	Clock
        磁盘最小值	Min_Disk
        磁盘平均值	AVG_Disk
        磁盘最大值	Max_Disk
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Sdisk(models.Model):
    '''
        宿主机磁盘趋势表
        标识	Id
        文件系统监控项	Name
        设备名称	Resource_Id
        时间戳	Clock
       磁盘最小值	Min_Disk
        磁盘平均值	AVG_Disk
        磁盘最大值	Max_Disk
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ResourceId = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ydisk(models.Model):
    '''
        云主机磁盘趋势表
        标识	Id
        文件系统监控项	Name
        设备名称	Cloud
        时间戳	Clock
       磁盘最小值	Min_Disk
        磁盘平均值	AVG_Disk
        磁盘最大值	Max_Disk
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ftf(models.Model):
    '''
        物理机网络流量均值表
        标识	Id
        设备名称	Server_Id
        时间戳	Clock
        监控项名    Name
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    ServerId = models.ForeignKey(Jk_Server, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ytf(models.Model):
    '''
        云主机网络流量均值表
          标识	Id
        设备名称	Cloud _Id
        时间戳	Clock
        监控项名    Name
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    CloudId = models.ForeignKey(Jk_Cloud_Device, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Stf(models.Model):
    '''
        宿主机网络流量均值表
          标识	Id
        设备名称	Resource_Id
        监控项名    Name
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Resource_Id = models.ForeignKey(Jk_Resource_Host, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ctf(models.Model):
    '''
        存储网络流量均值表
            标识	Id
        设备名称	Storage_Id
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    StorageId = models.ForeignKey(Jk_Storage, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jtf(models.Model):
    '''
        交换机网络流量均值表
        标识	Id
        设备名称	Switches_Id
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ltf(models.Model):
    '''
        路由器网络流量均值表
         标识	Id
        设备名称	Routing_Id
        时间戳	Clock
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Name = models.CharField(max_length=256, null=True)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jdl(models.Model):
    '''
        交换机时延趋势表
        标识	Id
        时延监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        时延最小值	Min_Sy
        时延平均值	AVG_Sy
        时延最大值	Max_Sy
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Ldl(models.Model):
    '''
        路由器时延趋势表
        标识	Id
        时延监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
       时延最小值	Min_Sy
        时延平均值	AVG_Sy
        时延最大值	Max_Sy
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    RoutingId = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzconn(models.Model):
    '''
        负载均衡实连接均值表
        标识	Id
        实连接监控项	Name
        设备名称	Fz_id
        时间戳	Clock
        实连接最小值	Min_conn
实连接平均值	AVG_conn
实连接最大值	Max_conn
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Fzxconn(models.Model):
    '''
        负载均衡虚连接数均值表
        标识	Id
        虚连接数监控项	Name
        设备名称	Fz_id
        时间戳	Clock
        虚连接数最小值	Min_xconn
虚连接数平均值	AVG_xconn
虚连接数最大值	Max_xconn
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    FzId = models.ForeignKey(Jk_Fz, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Jnet(models.Model):
    '''
        交换机带宽利用率均值表
        标识	Id
        带宽利用率监控项	Name
        设备名称	Switches_Id
        时间戳	Clock
        带宽利用率最小值	Min_Dk
带宽利用率平均值	AVG_Dk
带宽利用率最大值	Max_Dk
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    SwitchesId = models.ForeignKey(Jk_Switches, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Lnet(models.Model):
    '''
        路由器带宽利用率均值表
        标识	Id
        带宽利用率监控项	Name
        设备名称	Routing_Id
        时间戳	Clock
        带宽利用率最小值	Min_Dk
带宽利用率平均值	AVG_Dk
带宽利用率最大值	Max_Dk
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    Routing_Id = models.ForeignKey(Jk_Routing, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_FwSes(models.Model):
    '''
        防火墙会话数均值表
        标识	Id
        会话数监控项	Name
        设备名称	Fw_id
        时间戳	Clock
        会话数最小值	Min_Hh
        会话数平均值	AVG_Hh
        会话数最大值	Max_Hh
         描述	DESC
    '''
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=256, null=False)
    Fw_id = models.ForeignKey(Jk_Fw, max_length=8)
    Clock = models.IntegerField(null=False)
    Min_Value = models.CharField(max_length=256, null=True)
    AVG_Value = models.CharField(max_length=256, null=True)
    Max_Value = models.CharField(max_length=256, null=True)
    DESC = models.CharField(max_length=128)


class Jk_Mt_Status(models.Model):
    '''
        维护状态表
        维护状态标识	Mt_id
        维护状态名称	Mt_Staus_Name
        描述	DESC
    '''
    MtStausName = models.CharField(max_length=16, null=False)
    DESC = models.CharField(max_length=128, null=True)


class Jk_Mt_Information(models.Model):
    '''
        维护状态表
        维护标识	Mt_ Information _id
        设备Ip	Ip
        设备名	Name
        发生时间	Oc_time
        结束时间	End_time
        维护状态	Mt_id
        上线标识    maintenanceid
        描述	DESC
        'Mt_Status_id':'维护标识',
        'Ip':'设备Ip',
        'Name':'设备名',
        'Oc_time':'发生时间',
        'End_time':'结束时间',
        'hostid':'hostid',
        'groupid':'所属设备组':
        'maintenanceid':'上线标识',
        'DESC':'描述',
    '''

    ip = models.CharField(max_length=32, null=True)
    Name = models.CharField(max_length=256, null=True)
    Oc_time = models.IntegerField(null=True)
    End_time = models.IntegerField(null=True)
    hostid = models.IntegerField(null=True)
    groupid = models.ForeignKey(JK_Shebei_Group)
    maintenanceid = models.IntegerField(null=True)
    DESC = models.CharField(max_length=128, null=True)


class ServerToZabbix(models.Model):
    """物理机"""
    hostname = models.CharField(max_length=64)  # Server Name
    host_ip = models.CharField(max_length=64, blank=True)
    app_name = models.CharField(max_length=64, blank=True)
    user = models.CharField(max_length=64, null=True, blank=True)
    park = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)  # Machine room
    rock = models.CharField(max_length=64, null=True, blank=True)  # Rcck Name
    U_start = models.CharField(max_length=64, blank=True)
    U_stop = models.CharField(max_length=64, blank=True)
    data_center = models.CharField(max_length=64, blank=True)
    vendors = models.CharField(max_length=128, null=True, blank=True)
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'server_2_zabbix'


class CloudDeviceToZabbix(models.Model):
    """云主机"""
    hostname = models.CharField(max_length=64)  # Server Name
    host_ip = models.CharField(max_length=64, blank=True)
    app_name = models.CharField(max_length=64, blank=True)
    user = models.CharField(max_length=64, null=True, blank=True)
    park = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)  # Machine room
    rock = models.CharField(max_length=64, null=True, blank=True)  # Rcck Name
    U_start = models.CharField(max_length=64, blank=True)
    U_stop = models.CharField(max_length=64, blank=True)
    data_center = models.CharField(max_length=64, blank=True)
    vendors = models.CharField(max_length=128, null=True, blank=True)
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'cloud_cevice_2_zabbix'


class ResourceHostToZabbix(models.Model):
    """宿主机"""
    hostname = models.CharField(max_length=64)  # Server Name
    host_ip = models.CharField(max_length=64, blank=True)
    app_name = models.CharField(max_length=64, blank=True)
    user = models.CharField(max_length=64, null=True, blank=True)
    park = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)  # Machine room
    rock = models.CharField(max_length=64, null=True, blank=True)  # Rcck Name
    U_start = models.CharField(max_length=64, blank=True)
    U_stop = models.CharField(max_length=64, blank=True)
    data_center = models.CharField(max_length=64, blank=True)
    vendors = models.CharField(max_length=128, null=True, blank=True)
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True, verbose_name=_("¼¯Èº"))

    class Meta:
        db_table = 'resource_host_2_zabbix'


class StorageToZabbix(models.Model):
    """´存储"""
    hostname = models.CharField(max_length=64)  # Server Name
    host_ip = models.CharField(max_length=64, blank=True)
    app_name = models.CharField(max_length=64, blank=True)
    user = models.CharField(max_length=64, null=True, blank=True)
    park = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)  # Machine room
    rock = models.CharField(max_length=64, null=True, blank=True)  # Rcck Name
    U_start = models.CharField(max_length=64, blank=True)
    U_stop = models.CharField(max_length=64, blank=True)
    data_center = models.CharField(max_length=64, blank=True)
    vendors = models.CharField(max_length=128, null=True, blank=True)
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î

    class Meta:
        db_table = 'storage_2_zabbix'


class NetworkDeviceToZabbix(models.Model):
    """网络设备¸"""
    hostname = models.CharField(max_length=64)  # Server Name
    host_ip = models.CharField(max_length=64, blank=True)
    app_name = models.CharField(max_length=64, blank=True)
    user = models.CharField(max_length=64, null=True, blank=True)
    park = models.CharField(max_length=64, null=True, blank=True)
    room = models.CharField(max_length=64, null=True, blank=True)  # Machine room
    rock = models.CharField(max_length=64, null=True, blank=True)  # Rcck Name
    U_start = models.CharField(max_length=64, blank=True)
    U_stop = models.CharField(max_length=64, blank=True)
    data_center = models.CharField(max_length=64, blank=True)
    vendors = models.CharField(max_length=128, null=True, blank=True)
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    device_type = models.CharField(max_length=64)  # Server Name

    class Meta:
        db_table = 'network_nevice_2_zabbix'
        

class Jk_pass(models.Model):
    '''
    接口所需zabbix的用户名和密码
    '''
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=512)
    zabbix_id = models.IntegerField()
    url = models.CharField(max_length=126)
