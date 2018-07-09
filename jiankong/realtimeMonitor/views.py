#-*- coding: UTF-8 -*-
import time
import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from django.db.models import Q,F

from dashBoard.models import *
import xlwt
import datetime
import io
from io import StringIO,BytesIO

from signbackInformation.views import  get_ip_list


# Create your views here.



#告警超时数
from dashBoard.models import ServerToZabbix, ResourceHostToZabbix, CloudDeviceToZabbix


def getcs(user, lev, timedur):
    iplist = get_ip_list(user)
    starttime = time.time()
    if int(timedur) == 0:
        timedur = time.time() - 7*24*3600
    else:
        timedur = time.time() - 30*24*3600
    # alertcs = Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)        #当前告警超时
    alertcs = Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)        #当前告警超时
    # alerthiscs = Jk_Alert_His.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)   #历史告警超时
    alerthiscs = AlertHis.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)   #历史告警超时
    count = 0

    for alert in alertcs:
        # if starttime - alert.Oc_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600: # 修改
        if starttime - alert.Oc_time > int(Fault.objects.get(Fault_id=lev).DESC) * 3600:
            count += 1
    for alerthis in alerthiscs:
        # if alerthis.Oc_time - alerthis.End_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600: # 修改
        if alerthis.Oc_time - alerthis.End_time > int(Fault.objects.get(Fault_id=lev).DESC) * 3600:
            count += 1

    return count





#应用告警
def ztalarmEvent(user):
    # if request.method == 'GET':
        alertlist = []
        alertzd = 0
        alertyz = 0
        alertyb = 0
        alertqt = 0
        iplist = get_ip_list(user)
        typelist = []

        #应用类型

        # apps = Jk_App.objects.filter(App_admin=user) # 修改
        apps = App.objects.filter(App_admin=user)
        AppList = []

        for app in apps:
            AppList.append(app.AppName)

        #告警应用类别
        zdapplist = []
        yzapplist = []
        ybapplist = []
        qtapplist = []

        #所有属于所管理应用的告警
        # alerts = Jk_alert.objects.filter(Application__in=AppList) # 修改
        alerts = Alert.objects.filter(Application__in=AppList)
        for j in AppList:

            # zdapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4) # 修改
            zdapplist.append({"value": Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4)
                             .filter(Application=j).count(),
                              # "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4)
                              "name": str(j)+":"+str(Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4)
                             .filter(Application=j).count())})

            # yzapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3) # 修改
            yzapplist.append({"value": Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3)
                             .filter(Application=j).count(),
                              # "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3) # 修改
                              "name": str(j)+":"+str(Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3)
                             .filter(Application=j).count())})

            # ybapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2) #修改
            ybapplist.append({"value": Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2)
                             .filter(Application=j).count(),
                              # "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2) # 修改
                              "name": str(j)+":"+str(Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2)
                             .filter(Application=j).count())})

            # qtapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1) # 修改
            qtapplist.append({"value": Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1)
                             .filter(Application=j).count(),
                              # "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1) # 修改
                              "name": str(j)+":"+str(Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1)
                             .filter(Application=j).count())})

        # print(zdapplist)


        #告警分类
        for i in alerts:
            # zd = {"value": 0, "name": ""}
            if (i.Type_ip).strip() in iplist:
                alertlist.append(i)
                if i.Alert_lev_id_id == 4:
                    typelist.append(i.Type)
                    alertzd += 1
                elif i.Alert_lev_id_id == 3:
                    alertyz += 1
                elif i.Alert_lev_id_id == 2:
                    alertyb += 1
                else:
                    alertqt += 1


        #超时未超时
        cs = {"value": 0, "name": "超时"}
        wcs = {"value": 0, "name": "未超时"}

        cszd = {"value": 0, "name": '重大'}
        csyz = {"value": 0, "name": '严重'}
        csyb = {"value": 0, "name": '一般'}
        csqt = {"value": 0, "name": '其它'}
        wcsyz = {"value": 0, "name": '重大'}
        wcszd = {"value": 0, "name": '严重'}
        wcsyb = {"value": 0, "name": '一般'}
        wcsqt = {"value": 0, "name": '其它'}

        #超时未超时
        cslist = []
        wcslist = []
        for j in alerts:
            ctime = time.time()

            if (j.Type_ip).strip() in iplist:
                if (j.Alert_lev_id).Alert_lev_id == 4:
                    if int(ctime) - int(j.Oc_time) > 2 * 3600:
                        cs['value'] += 1
                        cszd["value"] +=1
                    else:
                        wcs['value'] += 1
                        wcszd["value"]+=1

                if (j.Alert_lev_id).Alert_lev_id == 3:
                    if int(ctime) - int(j.Oc_time) > 4 * 3600:
                        cs['value'] += 1
                        csyz["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyz["value"] += 1

                if (j.Alert_lev_id).Alert_lev_id == 2:
                    if int(ctime) - int(j.Oc_time) > 8 * 3600:
                        cs['value'] += 1
                        csyb["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyb["value"] += 1

                if (j.Alert_lev_id).Alert_lev_id == 1:
                    if int(ctime) - int(j.Oc_time) > 48 * 3600:
                        cs['value'] += 1
                        csqt["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsqt["value"] += 1
        wcs['name'] = "未超时:"+str(wcs['value'])
        cs['name'] = "超时:"+str(cs['value'])
        appinfo = {"appname":"应用名称","applev":"应用级别","appzd":"重大","appyz":"严重",
                   "appyb":"一般","appqt":"其它"}




        alertlevcount = {"alertzd": alertzd, "alertyz": alertyz, "alertyb": alertyb, "alertqt": alertqt,
                         "alertlist": alertlist, "cs": cs, "wcs": wcs, "wcszd": wcszd, "wcsyz": wcsyz,
                         "wcsyb": wcsyb, "wcsqt": wcsqt, "cszd": cszd, "csyz": csyz, "csyb": csyb, "csqt": csqt,
                         "zdapplist": zdapplist, "yzapplist": yzapplist, "ybapplist":ybapplist,
                         "qtapplist": qtapplist
                        }

        return alertlevcount


#应用告警详情
def GetAppAlert(request):
    appinfos = []
    # 应用类型
    if request.user == "Admin" or request.user == "admin":
        # apps = Jk_App.objects.all() # 修改
        apps = App.objects.all()
    else:
        # apps = Jk_App.objects.filter(App_admin=request.user) # 修改
        apps = App.objects.filter(App_admin=request.user)
    AppList = []
    for app in apps:
        AppList.append(app.AppName)

    for j in AppList:
        # for i in alerts:
        # 整体的进行修改
        # appzd = Jk_alert.objects.filter(Alert_lev_id_id=4).filter(Application=j).count()
        appzd = Alert.objects.filter(Alert_lev_id_id=4).filter(Application=j).count()

        # appyz = Jk_alert.objects.filter(Alert_lev_id_id=3).filter(Application=j).count()
        appyz = Alert.objects.filter(Alert_lev_id_id=3).filter(Application=j).count()

        # appyb = Jk_alert.objects.filter(Alert_lev_id_id=2).filter(Application=j).count()
        appyb = Alert.objects.filter(Alert_lev_id_id=2).filter(Application=j).count()

        # appqt = Jk_alert.objects.filter(Alert_lev_id_id=1).filter(Application=j).count()
        appqt = Alert.objects.filter(Alert_lev_id_id=1).filter(Application=j).count()

        # applev = Jk_App_lev.objects.get(App_lev_id=(Jk_App.objects.get(AppName=j).App_lev_id_id)).App_lev_Name # 修改
        applev = AppLev.objects.get(App_lev_id=(Jk_App.objects.get(AppName=j).App_lev_id_id)).App_lev_Name
        print(applev)
        appinfo = {
            "appname": j, "applev": applev, "appzd": appzd, "appyz": appyz,
            "appyb": appyb, "appqt": appqt
        }
        appinfos.append(appinfo)
    print(appinfos)
    datajson = {"code": 0, "msg": "", "count": len(appinfos), "data": appinfos}
    return HttpResponse(json.dumps(datajson))
    pass


#应用设备告警详情
@csrf_exempt
def getAppinfo(request):
    if request.method == "POST":
        appname = request.POST.get("appname", "")
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        iplist = get_ip_list(request.user)
        # print(pageIndex)
        # print(pageSize)
        alertlist = []
        # alerts = Jk_alert.objects.filter(Application=appname) # 修改
        alerts = Alert.objects.filter(Application=appname)
        count = 0
        total = len(alerts)
        for i in alerts[(pageIndex-1)*pageSize:pageIndex*pageSize]:

            if (i.Type_ip).strip() in iplist:

                if i.Status == 0:
                    status = "解决"
                else:
                    status = "未解决"

                if i.A_time:
                    atime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.A_time)))
                else:
                    atime = ""

                if i.Type == "物理机":
                    # print(i.Type_ip)
                    hostnames = ServerToZabbix.objects.filter(host_ip=i.Type_ip)[0].hostname
                    # for h in hostnames:
                    #     hostname = h
                elif i.Type == "宿主机":
                    hostnames = ResourceHostToZabbix.objects.filter(host_ip=i.Type_ip)[0].hostname
                    # for h in hostnames:
                    #     hostname = h
                elif i.Type == "云主机":
                    hostnames = CloudDeviceToZabbix.objects.filter(host_ip=i.Type_ip)[0].hostname
                    # for h in hostnames:
                    #     hostname = h
                elif i.Type == "网络交换机" or i.Type == "负载均衡" or i.Type == "防火墙":
                    hostnames = NetworkDeviceToZabbix.objects.filter(host_ip=i.Type_ip)[0].hostname
                    # for h in hostnames:
                    #     hostname = h

                alertlist.append({"Alert_lev_id": (i.Alert_lev_id).LevName, "Application": "Ucloud_Paas",
                                  "Type": i.Type, "hostname": hostnames, "message": i.message, "ip":i.Type_ip,
                                  "Oc_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.Oc_time))),
                                  "A_time": atime,
                                  "Sendto": i.Sendto, "Status": status, "item": i.item})
                count += 1
        # print(alertlist)
        alertjson = {"code": 0, "msg": "", "count": total, "data": alertlist}
        return HttpResponse(json.dumps(alertjson))
    else:
        alertjson = {"code": 0, "msg": "", "count": 0, "data": []}
        return HttpResponse(json.dumps(alertjson))
    pass





# 应用
def application(request):
    if request.method == 'GET':
        alertcount = ztalarmEvent(request.user)
        return render(request, 'realtimeMonitor/application.html',alertcount)
    elif request.method == 'POST':
        pass

# 应用信息
def applicationJump(request):
    if request.method == 'GET':
        appname = request.GET.get("appname", '')
        # appinfo = Jk_App.objects.get(AppName=appname) # 修改
        appinfo = App.objects.get(AppName=appname)
        # applev = Jk_App_lev.objects.get(App_lev_id=(Jk_App.objects.get(AppName=appname).App_lev_id_id)).App_lev_Name # 修改
        applev = AlertLev.objects.get(App_lev_id=(Jk_App.objects.get(AppName=appname).App_lev_id_id)).App_lev_Name
        # 应用详情
        content = {"appname": appinfo.AppName, "applev": applev, "appmedm": appinfo.App_Me_Dm,
                   "appmtdm": appinfo.App_Mt_Dm, "datacent": "KFCS", "approom": "1期402",
                   "appadmin": appinfo.App_admin, "appperson": appinfo.App_person}
        return render(request, 'realtimeMonitor/application-jump.html', content)

    elif request.method == 'POST':
        pass


# 设备厂商
def equipmentManufacturers(request):
    if request.method == 'GET':
        return render(request, 'realtimeMonitor/equipmentManufacturers.html')
    elif request.method == 'POST':
        pass


# 设备厂商 ---
def equipmentManufacturersJump(request):
    if request.method == 'GET':
        return render(request, 'realtimeMonitor/equipmentManufacturers-jump.html')
    elif request.method == 'POST':
        pass




#物理机
@csrf_exempt
def physicalMachine(request):
        if request.method == 'GET':
            iplists = get_ip_list(request.user)
            # servers = Jk_Server.objects.filter(IP__in=iplists) # 修改
            servers = Server.objects.filter(IP__in=iplists) # 修改
            #获取用户资源的物理机组
            groupids = []
            for server in servers:
                groupids.append(server.Group_id)
            # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
            group = DeviceGroup.objects.filter(id__in=groupids)

            return render(request, 'realtimeMonitor/physicalMachine.html',{'group':group})
        elif request.method == 'POST':
            ip = request.POST.get('ip', '')
            group = request.POST.get('group', '')
            pageIndex = int(request.POST.get('page',''))
            pageSize = int(request.POST.get('limit',''))
            iplist = get_ip_list(request.user)
            # p_list = Jk_Server.objects.filter(IP__in=iplist) # 修改
            p_list = Server.objects.filter(IP__in=iplist)
            searchiplist = ip.split(",")

            if ip != '':
                p_list = p_list.filter(IP__in =searchiplist)

                # if group != '':
                #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
                #     p_list = p_list.filter(Group = groupinfo)
            else:
                if group != '':
                    # groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                    groupinfo = DeviceGroup.objects.get(id=int(group))
                    p_list = p_list.filter(Group=groupinfo)



        res = []
        totalCount = len(p_list)

        for p in p_list[(pageIndex-1)*pageSize:pageIndex*pageSize]:
            res.append({"id":p.Server_id,"hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id, "hostname":p.ServerName,
                        "ip":p.IP,"group":p.Group.Group_Name,"status":p.Agent,
                        "zabbix_id":p.Group.Zabbix_id,"app":ServerToZabbix.objects.get(host_ip=p.IP).app_name})
        res = {
            "code":0,
            "msg":"",
            "count":totalCount,
            "data":res
        }
        return HttpResponse(json.dumps(res), content_type='application/json')



# def export_physicalMachine(request):
#     workbook = xlwt.Workbook(encoding='ascii')
#     worksheet = workbook.add_sheet('My Worksheet')
#     header = [u'单点',u'但是v']
#     i = 0
#     # 表头
#     for each_header in header:
#         sheet.write(0,i,each_header)
#         i += 1
#     # 表体
#     row = 1
#     # for each_row in data_arrary:
#     #     col = 0
#     #     #填充每一行数据
#     #     for each_col in data_arrary:
#
#
#     worksheet.write(0, 0, 'Unformatted value')  # 不带样式的写入
#
#     worksheet.write(1, 0, 'Formatted value', style)  # 带样式的写入
#
#     workbook.save('formatting.xls')  # 保存文件


# --------宿主机
@csrf_exempt
def hosMachine(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all()
        iplists = get_ip_list(request.user)
        # servers = Jk_Resource_Host.objects.filter(Ip__in=iplists) # 修改
        servers = ResourceHost.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)
        # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
        group = DeviceGroup.objects.filter(id__in=groupids)
        return render(request, 'realtimeMonitor/hosMachine.html', {'group': group})
    elif request.method == 'POST':
        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page',''))
        pageSize = int(request.POST.get('limit',''))
        # p_list = Jk_Resource_Host.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)
        # p_list = Jk_Resource_Host.objects.filter(Ip__in=iplist) # 修改
        p_list = ResourceHost.objects.filter(Ip__in=iplist)
        if ip != '':
            p_list = p_list.filter(Resource_Name__in = searchiplist)
            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group = groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)


    res = []
    totalCount = len(p_list)

    for p in p_list[(pageIndex-1)*pageSize:pageIndex*pageSize]:
        # res.append(
        #            # {"id": p.pk, "hostname": p.Resource_Name, "ip": p.IP, "group": p.Group.Group_Name, "status": p.Agent})
        res.append({"id": p.pk,"hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id, "hostname": p.Resource_Name,
                    "ip": p.Ip, "group": p.Group.Group_Name, "status": p.Agent,"datacenter":p.Center,
                    "jiqun":ResourceHostToZabbix.objects.get(host_ip=p.Ip).app_name})
    res = {
        "code":0,
        "msg":"",
        "count":totalCount,
        "data":res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# --------云主机
@csrf_exempt
def cloudHost(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all()
        iplists = get_ip_list(request.user)
        # servers = Jk_Cloud_Device.objects.filter(Ip__in=iplists) # 修改
        servers = CloudDevice.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)
        # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
        group = DeviceGroup.objects.filter(id__in=groupids)

        center = CloudDeviceToZabbix.objects.all()
        return render(request, 'realtimeMonitor/cloudHost.html',{"group":group,"center":center})
    elif request.method == 'POST':
        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page',''))
        pageSize = int(request.POST.get('limit',''))
        # p_list = Jk_Cloud_Device.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)

        # p_list = Jk_Cloud_Device.objects.filter(Ip__in=iplist) # 修改
        p_list = CloudDevice.objects.filter(Ip__in=iplist)

        if ip != '':
            p_list = p_list.filter(Ip__in =searchiplist)

            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group = groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group))
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)

    res = []
    totalCount = len(p_list)

    for p in p_list[(pageIndex-1)*pageSize:pageIndex*pageSize]:
        # res.append(
        #            # {"id": p.pk, "hostname": p.Resource_Name, "ip": p.IP, "group": p.Group.Group_Name, "status": p.Agent})
        res.append({"id": p.pk,"hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id, "hostname": p.CloudDeviceName,
                    "ip": p.Ip, "group": p.Group.Group_Name, "garden":CloudDeviceToZabbix.objects.get(host_ip=p.Ip).park,"status": p.Agent,
                    "datacenter":CloudDeviceToZabbix.objects.get(host_ip=p.Ip).data_center,
                    "jiqun":CloudDeviceToZabbix.objects.get(host_ip=p.Ip).cluster,
                    "app":CloudDeviceToZabbix.objects.get(host_ip=p.Ip).app_name})
    res = {
        "code":0,
        "msg":"",
        "count":totalCount,
        "data":res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# 储存
# --------磁盘阵列
@csrf_exempt
def diskArray(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all() # 修改
        group = DeviceGroup.objects.all()
        return render(request, 'realtimeMonitor/diskArray.html',{'group':group})
    elif request.method == 'POST':
        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        # p_list = Jk_Sdisk_Pf_Ids.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)
        #p_list = Jk_Storage.objects.filter(Ip__in=iplist) # 修改
        p_list = Storage.objects.filter(Ip__in=iplist)
        if ip != '':
            p_list = p_list.filter(IP__in=searchiplist)

            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group=groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)

    res = []
    totalCount = len(p_list)

    for p in p_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
        res.append({"id": p.pk, "hostname": p.Name, "ip": "", "group": p.Group.Group_Name, "status": ""})
    res = {
        "code": 0,
        "msg": "",
        "count": totalCount,
        "data": res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# --------光纤交换机
def fiberOpticSwitch(request):
    if request.method == 'GET':
        return render(request, 'realtimeMonitor/fiberOpticSwitch.html')
    elif request.method == 'POST':
        pass

# 网络设备
# --------交换机
@csrf_exempt
def switches(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all()
        iplists = get_ip_list(request.user)
        # servers = Jk_Switches.objects.filter(Ip__in=iplists) # 修改
        servers = Switches.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)
        # group = JK_Shebei_Group.objects.filter(id__in=groupids) #修改
        group = DeviceGroup.objects.filter(id__in=groupids)

        return render(request, 'realtimeMonitor/switches.html',{"group":group})
    elif request.method == 'POST':

        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        # p_list = Jk_Switches.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)

        # p_list = Jk_Switches.objects.filter(Ip__in=iplist) #修改
        p_list = Switches.objects.filter(Ip__in=iplist)

        if ip != '':
            p_list = p_list.filter(SwitchesName__in=searchiplist)
            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group=groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)

    res = []
    totalCount = len(p_list)


    for p in p_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
        res.append({"id": p.pk,"hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id, "hostname": p.SwitchesName,
                    "ip": p.Ip, "group": p.Group.Group_Name, "status": p.status})
    res = {
        "code": 0,
        "msg": "",
        "count": totalCount,
        "data": res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# --------路由器
@csrf_exempt
def router(request):
    if request.method == 'GET':
        iplists = get_ip_list(request.user)
        # servers = Jk_Routing.objects.filter(Ip__in=iplists) # 修改
        servers = Routing.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)

        # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
        group = DeviceGroup.objects.filter(id__in=groupids)

        # group = JK_Shebei_Group.objects.all()
        return render(request, 'realtimeMonitor/router.html',{'group':group})
    elif request.method == 'POST':
        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        # p_list = Jk_Routing.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)

        # p_list = Jk_Routing.objects.filter(Ip__in=iplist) # 修改
        p_list = Routing.objects.filter(Ip__in=iplist)

        if ip != '':
            p_list = p_list.filter(RoutingName__in=searchiplist)

            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group=groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group))
                groupinfo = DeviceGroup.objects.get(id=int(group))

                p_list = p_list.filter(Group=groupinfo)

    res = []

    totalCount = len(p_list)
    for p in p_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]:

        res.append(
            {"id": p.pk, "hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id,"hostname": p.RoutingName,
             "ip": p.Ip, "group": p.Group.Group_Name,"status": p.status})
    res = {
        "code": 0,
        "msg": "",
        "count": totalCount,
        "data": res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# --------负载均衡
@csrf_exempt
def loadBalancing(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all()
        iplists = get_ip_list(request.user)
        # servers = Jk_Fz.objects.filter(Ip__in=iplists) # 修改
        servers = Fz.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)
        # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
        group = DeviceGroup.objects.filter(id__in=groupids)
        return render(request, 'realtimeMonitor/loadBalancing.html',{'group':group})
    elif request.method == 'POST':


        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        # p_list = Jk_Fz.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)
        # 修改
        # p_list = Jk_Fz.objects.filter(Ip__in=iplist)
        p_list = Fz.objects.filter(Ip__in=iplist)
        if ip != '':
            p_list = p_list.filter(Fz_name__in=searchiplist)

            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group=groupinfo)
        else:
            if group != '':
                # groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)

    res = []

    totalCount = len(p_list)
    fz_ping = Jk_Fzping_Pf_Ids.objects.all()
    fz_relnum = Jk_Fzconn_Pf_Ids.objects.all()
    fz_badnum = Jk_Fzxconn_Pf_Ids.objects.all() # 缺少字段
    for p in p_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
        pingstatus = fz_ping.filter(Fz_id=p.Fz_id)
        if pingstatus.count() == 0:
            pingstatus = ''
        else:
            pingstatus = pingstatus[0].Value
        if pingstatus == '1':
            pingstatus = '通'
        elif pingstatus == '0':
            pingstatus = "不通"
        relnum = fz_relnum.filter(Fz_id = p.Fz_id)
        badnum = fz_badnum.filter(Fz_id = p.Fz_id)
        if relnum.count() == 0:
            relnum = ''
        else:
            relnum = relnum[0].Value
        if badnum.count() == 0:
            badnum = ''
        else:
            badnum = badnum[0].Value
        res.append(
            {"id": p.pk, "hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id,"hostname": p.Fz_name,
             "ip": p.Ip, "group": p.Group.Group_Name,"relnum":"","badnum":"", "pingstatus": pingstatus, "status": "",
             "status": p.status})
    res = {
        "code": 0,
        "msg": "",
        "count": totalCount,
        "data": res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# --------防火墙
@csrf_exempt
def firewall(request):
    if request.method == 'GET':
        # group = JK_Shebei_Group.objects.all()
        iplists = get_ip_list(request.user)
        # servers = Jk_Fw.objects.filter(Ip__in=iplists) # 修改
        servers = Fw.objects.filter(Ip__in=iplists)
        # 获取用户资源的物理机组
        groupids = []
        for server in servers:
            groupids.append(server.Group_id)
        # group = JK_Shebei_Group.objects.filter(id__in=groupids) # 修改
        group = DeviceGroup.objects.filter(id__in=groupids)
        return render(request, 'realtimeMonitor/firewall.html',{"group":group})
    elif request.method == 'POST':
        ip = request.POST.get('ip', '')
        group = request.POST.get('group', '')
        pageIndex = int(request.POST.get('page',''))
        pageSize = int(request.POST.get('limit',''))
        # p_list = Jk_Fw.objects.all()
        searchiplist = ip.split(",")
        iplist = get_ip_list(request.user)
        # p_list = Jk_Fw.objects.filter(Ip__in=iplist) # 修改
        p_list = Fw.objects.filter(Ip__in=iplist)
        if ip != '':
            p_list = p_list.filter(Fw_name__in =searchiplist)
            # if group != '':
            #     groupinfo = JK_Shebei_Group.objects.get(id=int(group))
            #     p_list = p_list.filter(Group = groupinfo)
        else:
            if group != '':
                groupinfo = JK_Shebei_Group.objects.get(id=int(group)) # 修改
                groupinfo = DeviceGroup.objects.get(id=int(group))
                p_list = p_list.filter(Group=groupinfo)

    res = []
    totalCount = len(p_list)
    fw_ping = Jk_Fwping_Pf_Ids.objects.all() # 缺少表
    for p in p_list[(pageIndex-1)*pageSize:pageIndex*pageSize]:
        pingstatus = fw_ping.filter(Fw_id=p.Fw_id)[0].Value
        if pingstatus == '1':
            pingstatus = '通'
        elif pingstatus == '0':
            pingstatus = "不通"

        res.append({"id":p.pk,"hostid":p.Hostid,"Zabbix_id":p.Group.Zabbix_id,
                    "hostname":p.Fw_name,"ip":p.Ip,"group":p.Group.Group_Name,"pingstatus":pingstatus,"status":"","status":p.status})
    res = {
        "code":0,
        "msg":"",
        "count":totalCount,
        "data":res
    }
    return HttpResponse(json.dumps(res), content_type='application/json')



@csrf_exempt
def exportPhysicalMachine(request):
    data_list = request.POST.getlist('data_list')
    check_list = request.POST.getlist('check_list')
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=user.xls'
    wb = xlwt.Workbook(encoding='utf-8')

    for item in data_list:
        print (item)
        if item == u'CPU利用率':
            print('2'*100)
            sheet = wb.add_sheet(u'物理机CPU利用率')
            print(sheet)

            # 写标题栏
            sheet.write(0, 0, '主机IP')
            sheet.write(0, 1, 'CPU最大利用率', )
            sheet.write(0, 2, 'CPU最小利用率',)
            sheet.write(0, 3, 'CPU平均利用率',)
            row = 1
            for item in check_list:
                result_list = Jk_Server_Rpt.objects.filter(Server_Id=item)
                for result in result_list:
                    sheet.write(row, 0, '',)
                    sheet.write(row, 1, usa.Cpu_Max_Usage,)
                    sheet.write(row, 2, usa.Cpu_Min_Usage,)
                    sheet.write(row, 3, usa.Cpu_Avg_Usage,)
                row  = row + 1
            # 写出到IO
            print('5' * 100)
            output = io.StringIO()

            print('6' * 100)
            wb.encoding='gbk'
            wb.save(output)
            print('7' * 100)
            # 重新定位到开始
            output.seek(0)
            print('8' * 100)
            response.write(output.getvalue())
            print(response)
            print('9' * 100)
            return response
        # if item == u'内存利用率':
        #     pass
        # if item == u'磁盘使用率':
        #     pass
        # if item == u'网络流量':
        #     pass






