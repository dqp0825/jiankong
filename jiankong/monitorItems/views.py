# coding:utf-8
import base64

from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pyzabbix import ZabbixAPI
import json

# from dashBoard.models import Jk_Storage,Jk_Server,Jk_Cloud_Device,Jk_Resource_Host
# 修改
from dashBoard.models import Storage,Server,CloudDevice,ResourceHost
# from dashBoard.models import Jk_Fw,Jk_Fz,Jk_Switches,JK_Shebei_Group,Jk_pass
# 修改
from dashBoard.models import Fw,Fz,Switches,DeviceGroup,ZabbixPass
from dashBoard.models import ServerToZabbix,CloudDeviceToZabbix,ResourceHostToZabbix
# from dashBoard.models import StorageToZabbix,NetworkDeviceToZabbix,Jk_User
# 修改
from dashBoard.models import StorageToZabbix,NetworkDeviceToZabbix,User
# from dashBoard.models import Jk_Server,Jk_Cloud_Device,Jk_Switches,Jk_Storage,Jk_Fw,Jk_Fz,Jk_Resource_Host
# 修改
from dashBoard.models import Server,CloudDevice,Switches,Storage,Fw,Fz,ResourceHost
from pyzabbix import ZabbixAPI
import json

from signbackInformation.views import  get_ip_list

# Create your views here.


user = "admin"

# 对整体的字段进行了修改
def getips(user):
    # userid = Jk_User.objects.filter(name=user).first().id # 修改
    userid = User.objects.filter(name=user).first().id
    # print(userid)
    # serverip = Jk_Server.objects.filter(User_id_id=userid)  # 修改
    serverip = Server.objects.filter(User_id_id=userid)
    # cloudip = Jk_Cloud_Device.objects.filter(User_id_id=userid)  # 修改
    cloudip = CloudDevice.objects.filter(User_id_id=userid)
    # resourceip = Jk_Resource_Host.objects.filter(User_id_id=userid)  # 修改
    resourceip = ResourceHost.objects.filter(User_id_id=userid)
    # storageip = Jk_Storage.objects.filter(User_id_id=userid)  # 修改
    storageip = Storage.objects.filter(User_id_id=userid)
    # switchip = Jk_Switches.objects.filter(User_id_id=userid)  # 修改
    switchip = Switches.objects.filter(User_id_id=userid)
    # fwip = Jk_Fw.objects.filter(User_id_id=userid)  # 修改
    fwip = Fw.objects.filter(User_id_id=userid)
    # fzip = Jk_Fz.objects.filter(User_id_id=userid)  # 修改
    fzip = Fz.objects.filter(User_id_id=userid)
    # resip = Jk_Resource_Host.objects.filter(User_id_id=userid) # 修改
    resip = ResourceHost.objects.filter(User_id_id=userid)
    iplist = {}
    for server in serverip:
        iplist[server.Hostid] = server.IP
        # iplist.append({server.Hostid:(server.host_ip).replace('\t','')})
    for cloud in cloudip:
        # iplist.append((cloud.host_ip).replace('\t',''))
        iplist[cloud.Hostid] = cloud.Ip
    for storage in storageip:
        # iplist.append((storage.host_ip).replace('\t',''))
        iplist[storage.Hostid] = storage.Ip
    for switch in switchip:
        # iplist.append((network.host_ip).replace('\t',''))
        iplist[switch.Hostid] = switch.Ip
    for resource in resourceip:
        # iplist.append((resource.host_ip).replace('\t',''))
        iplist[resource.Hostid] = resource.Ip
    for fw in fwip:
        # iplist.append((resource.host_ip).replace('\t',''))
        iplist[fw.Hostid] = fw.Ip
    for fz in fzip:
        # iplist.append((resource.host_ip).replace('\t',''))
        iplist[fz.Hostid] = fz.Ip
    for res in resip:
        # iplist.append((resource.host_ip).replace('\t',''))
        iplist[res.Hostid] = res.Ip
    return iplist



#应用
@csrf_exempt
def monitorItems(request):
        return render(request, 'monitorItems/monitoringIndicators.html')


def getgroupid(grouplist):
    groups = []
    for i in grouplist:
        # print(i.IP)
        groups.append(i)
    # print(groups)
    return groups


def gethostinfo(request):
    hostip = request.GET.get("ip", "")
    group = request.GET.get("group", "")
    iplist = get_ip_list(request.user)


    if hostip:
        storage = StorageToZabbix.objects.filter(host_ip=hostip).filter(user=request.user)
        server = ServerToZabbix.objects.filter(host_ip=hostip).filter(user=request.user)
        cloud = CloudDeviceToZabbix.objects.filter(host_ip=hostip).filter(user=request.user)
        resource = ResourceHostToZabbix.objects.filter(host_ip=hostip).filter(user=request.user)
        fws = NetworkDeviceToZabbix.objects.filter(host_ip=hostip)
        groupid = ''
        hostid = ''

        if storage:
            for host in storage:
                # groupid = Jk_Storage.objects.get(Ip=host.host_ip).Group_id # 修改
                groupid = Storage.objects.get(Ip=host.host_ip).Group_id
                # hostid = Jk_Storage.objects.get(Ip=host.host_ip).Hostid # 修改
                hostid = Storage.objects.get(Ip=host.host_ip).Hostid

        if server:
            for host in server:
                # groupid = Jk_Server.objects.get(IP=host.host_ip).Group_id # 修改
                groupid = Server.objects.get(IP=host.host_ip).Group_id
                # hostid = Jk_Server.objects.get(IP=host.host_ip).Hostid # 修改
                hostid = Server.objects.get(IP=host.host_ip).Hostid

        if cloud:
            for host in cloud:
                # groupid = Jk_Cloud_Device.objects.get(Ip=host.host_ip).Group_id # 修改
                groupid = CloudDevice.objects.get(Ip=host.host_ip).Group_id
                # hostid = Jk_Cloud_Device.objects.get(Ip=host.host_ip).Hostid # 修改
                hostid = CloudDevice.objects.get(Ip=host.host_ip).Hostid

        if resource:
            for host in resource:
                # groupid = Jk_Resource_Host.objects.get(Ip=host.host_ip).Group_id # 修改
                groupid = ResourceHost.objects.get(Ip=host.host_ip).Group_id
                # hostid = Jk_Resource_Host.objects.get(Ip=host.host_ip).Hostid #
                hostid = ResourceHost.objects.get(Ip=host.host_ip).Hostid

        if fws:
            for host in fws:
                if host.device_type == "交换机":
                    # groupid = Jk_Switches.objects.get(Ip=host.host_ip).Group_id # 修改
                    groupid = Switches.objects.get(Ip=host.host_ip).Group_id
                    # hostid = Jk_Switches.objects.get(Ip=host.host_ip).Hostid  # 修改
                    hostid = Switches.objects.get(Ip=host.host_ip).Hostid
                elif host.device_type == "防火墙":
                    # groupid = Jk_Fw.objects.get(Ip=host.host_ip).Group_id # 修改
                    groupid = Fw.objects.get(Ip=host.host_ip).Group_id
                    # hostid = Jk_Fw.objects.get(Ip=host.host_ip).Hostid # 修改
                    hostid = Fw.objects.get(Ip=host.host_ip).Hostid
                elif host.device_type == "路由器":
                    # groupid = Jk_Storage.objects.get(Ip=host.host_ip).Group_id # 修改
                    hostid = Storage.objects.get(Ip=host.host_ip).Hostid
                else:
                    # groupid = Jk_Fz.objects.get(Ip=host.host_ip).Group_id # 修改
                    groupid = Fz.objects.get(Ip=host.host_ip).Group_id # 修改
                    # hostid = Jk_Fz.objects.get(Ip=host.host_ip).Hostid # 修改
                    hostid = Fz.objects.get(Ip=host.host_ip).Hostid
                # hostid = host.Hostid
        if groupid:
            # groupname = JK_Shebei_Group.objects.get(id=groupid).Group_Name # 修改
            groupname = DeviceGroup.objects.get(id=groupid).Group_Name
            # groupid = JK_Shebei_Group.objects.get(id=groupid).id # 修改
            groupid = DeviceGroup.objects.get(id=groupid).id

        return HttpResponse(json.dumps([{"ip":hostip,"group":groupname,"hostid":hostid,"groupid":groupid}]))




    if group:
        #获取查找的用户的设备组

        iplist = get_ip_list(request.user)
        grouplist = []
        # 修改
        # servergroup = Jk_Server.objects.filter(IP__in=iplist)
        servergroup = Server.objects.filter(IP__in=iplist)

        # rhostgroup = Jk_Resource_Host.objects.filter(Ip__in=iplist)
        rhostgroup = ResourceHost.objects.filter(Ip__in=iplist)

        # cloudgroup = Jk_Cloud_Device.objects.filter(Ip__in=iplist)
        cloudgroup = CloudDevice.objects.filter(Ip__in=iplist)

        # switchgroup = Jk_Switches.objects.filter(Ip__in=iplist)
        switchgroup = Switches.objects.filter(Ip__in=iplist)

        # routgroup = Jk_Storage.objects.filter(Ip__in=iplist)
        routgroup = Storage.objects.filter(Ip__in=iplist)

        # fwgroup = Jk_Fw.objects.filter(Ip__in=iplist)
        fwgroup = Fw.objects.filter(Ip__in=iplist)

        # fzgroup = Jk_Fz.objects.filter(Ip__in=iplist)
        fzgroup = Fz.objects.filter(Ip__in=iplist)


        # for i in servergroup:
        #     print(i.IP)


        grouplist.extend(getgroupid(servergroup))
        grouplist.extend(getgroupid(rhostgroup))
        grouplist.extend(getgroupid(cloudgroup))
        grouplist.extend(getgroupid(switchgroup))
        grouplist.extend(getgroupid(routgroup))
        grouplist.extend(getgroupid(fwgroup))
        grouplist.extend(getgroupid(fzgroup))


        groupidlist = []
        groupdict = {}
        for j in grouplist:
            groupidlist.append(j.Group_id)
            # groupdict[j.Group_id] = JK_Shebei_Group.objects.get(id=j.Group_id).Group_Name # 修改
            groupdict[j.Group_id] = DeviceGroup.objects.get(id=j.Group_id).Group_Name
        # print(groupidlist)
        # 修改
        # storage = Jk_Storage.objects.filter(Group_id__in=groupidlist)
        storage = Storage.objects.filter(Group_id__in=groupidlist)

        # server = Jk_Server.objects.filter(Group_id__in=groupidlist)
        server = Server.objects.filter(Group_id__in=groupidlist)

        # cloud = Jk_Cloud_Device.objects.filter(Group_id__in=groupidlist)
        cloud = CloudDevice.objects.filter(Group_id__in=groupidlist)

        # resource = Jk_Resource_Host.objects.filter(Group_id__in=groupidlist)
        resource = ResourceHost.objects.filter(Group_id__in=groupidlist)

        # fw = Jk_Fw.objects.filter(Group_id__in=groupidlist)
        fw = Fw.objects.filter(Group_id__in=groupidlist)

        # fz = Jk_Fz.objects.filter(Group_id__in=groupidlist)
        fz = Fz.objects.filter(Group_id__in=groupidlist)

        # sw = Jk_Switches.objects.filter(Group_id__in=groupidlist)
        sw = Switches.objects.filter(Group_id__in=groupidlist)
        datalist = []

        #获取查询组的设备信息
        if storage:
            for host in storage:
                datalist.append({"hostid":host.Hostid,"ip":host.Ip,"group":groupdict[host.Group_id],"groupid":host.Group_id})
        if server:
            for host in server:
                datalist.append({"hostid": host.Hostid, "ip": host.IP, "group": groupdict[host.Group_id],"groupid":host.Group_id})

        if cloud:
            for host in cloud:
                datalist.append({"hostid": host.Hostid, "ip": host.Ip, "group": groupdict[host.Group_id],"groupid":host.Group_id})

        if resource:
            for host in resource:
                datalist.append({"hostid": host.Hostid, "ip": host.Ip, "group": groupdict[host.Group_id],"groupid":host.Group_id})
        if fw:
            for host in fw:
                datalist.append({"hostid": host.Hostid, "ip": host.Ip, "group":groupdict[host.Group_id],"groupid":host.Group_id})

        if fz:
            for host in fz:
                datalist.append({"hostid": host.Hostid, "ip": host.Ip, "group": groupdict[host.Group_id],"groupid":host.Group_id})

        if sw:
            for host in sw:
                datalist.append({"hostid": host.Hostid, "ip": host.Ip, "group": groupdict[host.Group_id],"groupid":host.Group_id})

        return HttpResponse(json.dumps(datalist))
    return HttpResponse([])




#获取监控项
def getitem(request):
    hostid = request.GET.get("hostid", '')
    groupid = request.GET.get("groupid", '')
    print(hostid,groupid)
    # print("11111111111111")
    # zabbix_id = JK_Shebei_Group.objects.filter(id=groupid).first() # 修改
    zabbix_id = DeviceGroup.objects.filter(id=groupid).first()
    zbxid = zabbix_id.Zabbix_id
    print(zbxid)
    # urlob = Jk_pass.objects.filter(zabbix_id=zbxid).first() # 修改
    urlob = Pass.objects.filter(zabbix_id=zbxid).first()
    zabbixurl = urlob.url
    zapi = ZabbixAPI(zabbixurl)
    zapi.login("admin", "zabbix")
    items = zapi.item.get(hostids=hostid)

    return HttpResponse(json.dumps(items))
