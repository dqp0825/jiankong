from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.db import models


# Create your models here.
class User(models.Model):
    '''
        用户信息
        标识	id
        用户名	name
        用户名密码	Pwd
        描述	desc
    '''
    name = models.CharField(max_length=64, null=False)
    pwd = models.CharField(max_length=128, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'user'


class DeviceGroup(models.Model):
    '''
    设备组表
    标识 id
    组名称    group_Name
    组标记    group_id
    描述 desc
    服务端标识  zabbix_id
    '''
    name = models.CharField(max_length=64, null=False)
    group_id = models.CharField(max_length=8, null=False)
    # user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="device_groups")
    zabbix_id = models.IntegerField(null=True)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'device_group'


class DeviceType(models.Model):
    '''
        设备类型表
        设备类型名称：Server：服务器（物理机/宿主机/云主机/存储）
                      Switches:网络设备（交换机/负载均衡/防火墙/路由器）
        描述
    '''
    name = models.CharField(max_length=16, null=False)
    desc = models.CharField(max_length=64, null=True, blank=True, default='')

    class Meta:
        db_table = 'device_type'


class Switches(models.Model):
    '''
        交换机
        zabbix的hostid       hostid
        交换机名称	name
        Ip地址	ip
        所属设备组	group
        所属用户	user
        备注	desc
        SNMP状态	status
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=64, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name="switches")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="switches")
    status = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'switches'


class Storage(models.Model):
    '''
        存储设备表
        存储名称	name
        Ip地址	ip
        所属组	group
        所属用户	user
        备注	desc
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=32, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name="storages")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="storages")
    agent = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'storage'


class Fz(models.Model):
    '''
   标识	Fz_id
	    hostid
    负载均衡名称	Fz_name
    Ip地址	ip
    所属设备组	group
    所属用户	user
    备注	desc
    SNMP状态	status
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=64, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name="fzs")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="fzs")
    status = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'fz'


class ResourceHost(models.Model):
    '''
    宿主机ID	Resource_Id
	            hostid
    主机名	Resource_Name
    主机IP	ip
    所属设备组	group
    所属用户	user
    描述	desc
    Agent状态	agent
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=32, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="resource_hosts")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="resource_hosts")
    agent = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'resource_host'


class CloudDevice(models.Model):
    '''
    云主机表
    云主机名称	 name
    所属用户	user
    主机IP	ip
    所属组	group
    Agent状态	agent
    描述	desc
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=32, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="cloud_devices")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="cloud_devices")
    agent = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'cloud_device'


class DeviceLev(models.Model):
    '''
        设备型号表
        设备型号名称	DeviceLevName
        描述	DeviceLevDesc
    '''
    name = models.CharField(max_length=32, null=False)
    desc = models.CharField(max_length=64, null=True,blank=True, default='')

    class Meta:
        db_table = 'device_lev'


class Routing(models.Model):
    '''
        路由器
       标识	Routing_Id
	        hostid
        路由器名称	name
        Ip地址	ip
        所属设备组	group
        所属应用	Application
        所属用户	user
        备注	desc
        SNMP状态	status
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=64, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="routings")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="routings")
    status = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'routing'


class Server(models.Model):
    '''
        物理机表
                     hostid
        物理机名称	ServerName
        厂商	Vendor
        设备型号	DeviceLev
        设备IP	     ip
        设备数量	Num
        所属设备组	group
        所属应用	Application_id
        所属用户	User_id
        描述	desc
        Agent状态	agent
    '''
    hostid = models.IntegerField()
    name = models.CharField(max_length=16, null=False)
    Vendor = models.IntegerField(null=True)
    DeviceLev = models.ForeignKey(DeviceLev, null=True, blank=True, on_delete=models.SET_NULL, related_name="servers")
    ip = models.CharField(max_length=64, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="servers")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="servers")
    agent = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'server'


class Fw(models.Model):
    '''
    防火墙
    标识	Fw_id
	        hostid
    负载均衡名称	name
    Ip地址	ip
    所属设备组	group
    所属用户	user
    备注	desc
    SNMP状态	status
    '''
    # Fw_id = models.AutoField(primary_key=True)
    hostid = models.IntegerField()
    name = models.CharField(max_length=64, null=False)
    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="fws")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="fws")
    status = models.CharField(max_length=20, null=False)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'fw'


class AlertLev(models.Model):
    '''
        告警级别表
        级别名称	LevName
        描述	desc
    '''
    name = models.CharField(max_length=16, null=False)
    desc = models.CharField(max_length=64, null=True,blank=True, default='')

    class Meta:
        db_table = 'alert_lev'


class Fault(models.Model):
    '''
        故障等级	FaultName
        描述	desc
    '''
    name = models.CharField(max_length=64, null=False)
    desc = models.CharField(max_length=64, null=True,blank=True, default='')

    class Meta:
        db_table = 'fault'


class Alert(models.Model):
    '''
        告警信息表
        告警信息ID	id
        告警级别	lev
        所属设备类型	device_type
        所属设备	device_name
        所属设备ip	ip
        事件Id      eventid
        zabbix_id   zabbix_id
        告警内容	message
        发生时间	Oc_time
        受理时间	A_time
        通告人	    sendto
        受理结果 	status
        描述	    desc
    '''
    lev = models.ForeignKey(AlertLev, null=True, blank=True, on_delete=models.SET_NULL, related_name="alerts")
    item = models.CharField(max_length=128, blank=True, default='')
    eventid = models.CharField(max_length=20, blank=True, default='')
    zabbix_id = models.IntegerField()
    device_type = models.CharField(max_length=32, blank=True, default='')
    device_name = models.CharField(max_length=128, blank=True, default='')
    ip = models.CharField(max_length=20, null=False)
    message = models.TextField(null=True)
    oc_time = models.IntegerField(null=False)
    ack_time = models.IntegerField(null=True)
    sendto = models.CharField(max_length=64, blank=True, default='')
    status = models.IntegerField(null=True)
    desc = models.CharField(max_length=64, null=True,blank=True, default='')

    class Meta:
        db_table = 'alert'


class AlertHis(models.Model):
    '''
    告警信息历史表
    告警信息ID	id
    告警级别	lev
    所属应用	Application_id

    所属设备类型	device_type
    所属设备	device_name
    ip          ip

    告警内容	message
    发生时间	oc_time
    结束时间	end_time
    受理时间	a_time
    通告人	sendto
    受理结果 	status
    处理人	deal_person
    处理详情	deal_details
    处理完成时间	deal_end_time
    描述	desc
    '''
    lev = models.ForeignKey(AlertLev, null=True, blank=True, on_delete=models.SET_NULL, related_name="alert_hiss")

    eventid = models.CharField(max_length=20, blank=True, default='')
    zabbix_id = models.IntegerField()
    device_type = models.CharField(max_length=32, blank=True, default='')
    device_name = models.CharField(max_length=128, blank=True, default='')
    ip = models.CharField(max_length=20, null=False)
    item = models.CharField(max_length=128, blank=True, default='')
    message = models.TextField(null=False)
    oc_time = models.IntegerField(null=False)
    end_time = models.IntegerField(null=False)
    ack_time = models.IntegerField(null=True)
    sendto = models.CharField(max_length=64, null=False)
    status = models.IntegerField(null=True)
    deal_person = models.CharField(max_length=64, blank=True, default='')
    deal_details = models.TextField(null=True)
    deal_end_time = models.IntegerField(null=True)
    desc = models.CharField(max_length=64, null=True,blank=True, default='')

    class Meta:
        db_table = 'alert_his'


class MTInformation(models.Model):
    '''
        维护信息
        维护标识	Mt_ Information _id
        设备Ip	ip
        设备名	name
        发生时间	oc_time
        结束时间	end_time
        上线标识    maintenanceid
        描述	desc
    '''

    ip = models.CharField(max_length=32, null=True, blank=True, default='')
    name = models.CharField(max_length=256, blank=True, default='')
    oc_time = models.IntegerField(null=True)
    end_time = models.IntegerField(null=True)
    hostid = models.IntegerField(null=True)
    group = models.ForeignKey(DeviceGroup, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="mt_informations")
    maintenanceid = models.IntegerField(null=True)
    desc = models.CharField(max_length=128, null=True, blank=True, default='')

    class Meta:
        db_table = 'mtinformation'


class ServerToZabbix(models.Model):
    """物理机"""
    hostname = models.CharField(max_length=64)  # Server name
    host_ip = models.CharField(max_length=64, blank=True, default='')
    app_name = models.CharField(max_length=64, blank=True, default='')
    user = models.CharField(max_length=64, blank=True, default='')
    park = models.CharField(max_length=64, blank=True, default='')
    room = models.CharField(max_length=64, blank=True, default='')  # Machine room
    rock = models.CharField(max_length=64, blank=True, default='')  # Rcck name
    U_start = models.CharField(max_length=64, blank=True, default='')
    U_stop = models.CharField(max_length=64, blank=True, default='')
    data_center = models.CharField(max_length=64, blank=True, default='')
    vendors = models.CharField(max_length=128, blank=True, default='')
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        db_table = 'server_2_zabbix'


class CloudDeviceToZabbix(models.Model):
    """云主机"""
    hostname = models.CharField(max_length=64)  # Server name
    host_ip = models.CharField(max_length=64, blank=True, default='')
    app_name = models.CharField(max_length=64, blank=True, default='')
    user = models.CharField(max_length=64, blank=True, default='')
    park = models.CharField(max_length=64, blank=True, default='')
    room = models.CharField(max_length=64, blank=True, default='')  # Machine room
    rock = models.CharField(max_length=64, blank=True, default='')  # Rcck name
    U_start = models.CharField(max_length=64, blank=True, default='')
    U_stop = models.CharField(max_length=64, blank=True, default='')
    data_center = models.CharField(max_length=64, blank=True, default='')
    vendors = models.CharField(max_length=128, blank=True, default='')
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        db_table = 'cloud_cevice_2_zabbix'


class ResourceHostToZabbix(models.Model):
    """宿主机"""
    hostname = models.CharField(max_length=64)  # Server name
    host_ip = models.CharField(max_length=64, blank=True, default='')
    app_name = models.CharField(max_length=64, blank=True, default='')
    user = models.CharField(max_length=64, blank=True, default='')
    park = models.CharField(max_length=64, blank=True, default='')
    room = models.CharField(max_length=64, blank=True, default='')  # Machine room
    rock = models.CharField(max_length=64, blank=True, default='')  # Rcck name
    U_start = models.CharField(max_length=64, blank=True, default='')
    U_stop = models.CharField(max_length=64, blank=True, default='')
    data_center = models.CharField(max_length=64, blank=True, default='')
    vendors = models.CharField(max_length=128, blank=True, default='')
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    cluster = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        db_table = 'resource_host_2_zabbix'


class StorageToZabbix(models.Model):
    """´存储"""
    hostname = models.CharField(max_length=64)  # Server name
    host_ip = models.CharField(max_length=64, blank=True, default='')
    app_name = models.CharField(max_length=64, blank=True, default='')
    user = models.CharField(max_length=64, blank=True, default='')
    park = models.CharField(max_length=64, blank=True, default='')
    room = models.CharField(max_length=64, blank=True, default='')  # Machine room
    rock = models.CharField(max_length=64, blank=True, default='')  # Rcck name
    U_start = models.CharField(max_length=64, blank=True, default='')
    U_stop = models.CharField(max_length=64, blank=True, default='')
    data_center = models.CharField(max_length=64, blank=True, default='')
    vendors = models.CharField(max_length=128, blank=True, default='')

    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î

    class Meta:
        db_table = 'storage_2_zabbix'


class NetworkDeviceToZabbix(models.Model):
    """网络设备¸"""
    hostname = models.CharField(max_length=64)  # Server name
    host_ip = models.CharField(max_length=64, blank=True, default='')
    app_name = models.CharField(max_length=64, blank=True, default='')
    user = models.CharField(max_length=64, blank=True, default='')
    park = models.CharField(max_length=64, blank=True, default='')
    room = models.CharField(max_length=64, blank=True, default='')  # Machine room
    rock = models.CharField(max_length=64, blank=True, default='')  # Rcck name
    U_start = models.CharField(max_length=64, blank=True, default='')
    U_stop = models.CharField(max_length=64, blank=True, default='')
    data_center = models.CharField(max_length=64, blank=True, default='')
    vendors = models.CharField(max_length=128, blank=True, default='')
    # sn = models.CharField(max_length=128, blank=True)  # Î¨Ò»×Ö¶Î
    device_type = models.CharField(max_length=64, blank=True, default='')  # Server name

    class Meta:
        db_table = 'network_nevice_2_zabbix'


class ZabbixPass(models.Model):
    '''
    接口所需zabbix的用户名和密码
    '''
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=512)
    zabbix_id = models.IntegerField()
    url = models.CharField(max_length=126)

    class Meta:
        db_table = 'zabbix_pass'
