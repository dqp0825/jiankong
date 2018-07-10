# coding:utf8

import time
import json
import requests

from django.db.models import Q
from django.shortcuts import render, HttpResponse
from django import forms


from dashBoard.models import ServerToZabbix, CloudDeviceToZabbix, ResourceHostToZabbix, StorageToZabbix
from dashBoard.models import AlertLev, Alert, DeviceType, AlertHis, Fault, NetworkDeviceToZabbix, MTInformation
from signbackInformation.views import get_ip_list


class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)


# 首页
# @login_required
def index(request):
    url = "http://10.192.129.151/zabbix/api_jsonrpc.php"
    headers = {'Content-Type': 'application/json-rpc'}

    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "zabbix"
        },
        "id": 1
    }

    try:
        res = requests.post(url=url, data=json.dumps(data), headers=headers)
        auth = res.json().get("result")
    except Exception as e:
        auth = ''
    return render(request, "myindex.html", {"auth": auth})


# 获取用户的资源
def getips(user):
    k_ = ['serverip', 'cloudip', 'resourceip', 'storageip', 'networkip']
    v_ = [ServerToZabbix, CloudDeviceToZabbix, ResourceHostToZabbix, StorageToZabbix, NetworkDeviceToZabbix]
    ip_dic = {k: v.objects.filter(user=user) for k, v in zip(k_, v_)}

    # serverip = ServerToZabbix.objects.filter(user=user)
    # cloudip = CloudDeviceToZabbix.objects.filter(user=user)
    # resourceip = ResourceHostToZabbix.objects.filter(user=user)
    # storageip = StorageToZabbix.objects.filter(user=user)
    # networkip = NetworkDeviceToZabbix.objects.filter(user=user)

    ip_list = []
    for v in ip_dic.values():
        for p in v:
            ip_list.append(p.host_ip.replace('\t', ''))

    # for server in serverip:
    #     iplist.append((server.host_ip).replace('\t',''))
    # for cloud in cloudip:
    #     iplist.append((cloud.host_ip).replace('\t',''))
    # for storage in storageip:
    #     iplist.append((storage.host_ip).replace('\t',''))
    # for network in networkip:
    #     iplist.append((network.host_ip).replace('\t',''))
    # for resource in resourceip:
    #     iplist.append((resource.host_ip).replace('\t',''))
    return ip_list


# 告警完成数
def getyzend(user, lev, timedur):
    if int(timedur) == 0:
        timedur = time.time() - 7*24*3600
    else:
        timedur = time.time() - 30*24*3600
    ip_list = get_ip_list(user)
    # iplist = getips(user)
    # allalerthis = Jk_Alert_His.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=int(lev)).filter(End_time__gt=timedur).count() # 修改

    allalerthis = AlertHis.objects.filter(ip__in=ip_list).filter(id=int(lev)).filter(end_time__gt=timedur).count()
    return allalerthis


# 告警超时数
def getcs(user, lev, timedur):
    ip_list = get_ip_list(user)
    starttime = time.time()
    if int(timedur) == 0:
        timedur = time.time() - 7*24*3600
    else:
        timedur = time.time() - 30*24*3600
    alertcs = Alert.objects.filter(ip__in=ip_list).filter(id=lev).filter(oc_time__gt=timedur)        # 当前告警超时
    alerthiscs = AlertHis.objects.filter(ip__in=ip_list).filter(id=lev).filter(oc_time__gt=timedur)   # 历史告警超时
    count = 0

    for alert in alertcs:
        # if starttime - alert.Oc_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600:  # 修改
        if starttime - alert.oc_time > int(Fault.objects.get(id=lev).desc) * 3600:  # 修改
            count += 1
    for alerthis in alerthiscs:
        # if alerthis.End_time - alerthis.Oc_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600: # 修改
        if alerthis.end_time - alerthis.oc_time > int(Fault.objects.get(id=lev).desc) * 3600:
            count += 1

    return count


# 整体告警
def ztalarmEvent(user):
    # if request.method == 'GET':
        alertlist = []
        alertzd = 0
        alertyz = 0
        alertyb = 0
        alertqt = 0
        iplist = get_ip_list(user)
        typelist = []
        alerts = Alert.objects.all()
        types = DeviceType.objects.all()
        TypeList = []
        for type in types:
            TypeList.append(type.name)
        # 告警设备类型
        zdlist = []
        yzlist = []
        yblist = []
        qtlist = []
        AppList = []
        # 告警设备App
        # apps = Jk_App.objects.all() # 修改
        # apps = App.objects.all()

        # for app in apps:
        #     AppList.append(app.AppName)
        zdapplist = []
        yzapplist = []
        ybapplist = []
        qtapplist = []
    # 设备类型告警
        for i in TypeList:

            zdlist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(id=4).count(),
                           "name": str(i)+":"+str(Alert.objects.filter(device_type=i).filter(
                               ip__in=iplist).filter(id=4).count())})

            yzlist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(id=3).count(),
                           "name": str(i)+":"+str(Alert.objects.filter(device_type=i).filter(
                               ip__in=iplist).filter(id=3).count())})

            yblist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(id=2).count(),
                           "name": str(i)+":"+str(Alert.objects.filter(device_type=i).filter(
                               ip__in=iplist).filter(id=2).count())})

            qtlist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(id=1).count(),
                           "name": str(i)+":"+str(Alert.objects.filter(device_type=i).filter(
                               ip__in=iplist).filter(id=1).count())})


        # for i in alerts:
        #     # zd = {"value": 0, "name": ""}
        #     if (i.Type_ip).strip() in iplist:
        #         zdlist.append({"value": Jk_alert.objects.filter(Type=i).filter(
        #             Type_ip__in=iplist).filter(Alert_lev_id_id=4).count(), "name": i})

        # 应用告警
        # for j in AppList:
        #
        #     zdapplist.append({"value": Alert.objects.filter(ip__in=iplist).filter(id=4).count(),
        #                       "name": str(j)+":"+str(Alert.objects.filter(ip__in=iplist).filter(id=4).count())})
        #
        #     yzapplist.append({"value": Alert.objects.filter(ip__in=iplist).filter(id=3).count(),
        #                       "name": str(j)+":"+str(Alert.objects.filter(ip__in=iplist).filter(id=3).count())})
        #
        #     ybapplist.append({"value": Alert.objects.filter(ip__in=iplist).filter(id=2).count(),
        #                       "name": str(j)+":"+str(Alert.objects.filter(ip__in=iplist).filter(id=2).count())})
        #
        #     qtapplist.append({"value": Alert.objects.filter(ip__in=iplist).filter(id=1).count(),
        #                       "name": str(j)+":"+str(Alert.objects.filter(ip__in=iplist).filter(id=1).count())})

        # print(zdapplist)

        # 告警分类
        for i in alerts:
            # zd = {"value": 0, "name": ""}
            if i.ip.strip() in iplist:
                alertlist.append(i)
                if i.lev_id == 4:
                    typelist.append(i.device_type)
                    alertzd += 1
                elif i.lev_id == 3:
                    alertyz += 1
                elif i.lev_id == 2:
                    alertyb += 1
                else:
                    alertqt += 1

        # 超时未超时
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
        cslist = []
        wcslist = []
        for j in alerts:
            ctime = time.time()

            if j.ip.strip() in iplist:
                if j.lev.id == 1:
                    if int(ctime) - int(j.oc_time) > 2 * 3600:
                        cs['value'] += 1
                        cszd["value"] +=1
                    else:
                        wcs['value'] += 1
                        wcszd["value"] += 1

                if j.lev.id == 2:
                    if int(ctime) - int(j.oc_time) > 4 * 3600:
                        cs['value'] += 1
                        csyz["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyz["value"] += 1

                if j.lev.id == 3:
                    if int(ctime) - int(j.oc_time) > 8 * 3600:
                        cs['value'] += 1
                        csyb["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyb["value"] += 1

                if j.lev.id == 4:
                    if int(ctime) - int(j.oc_time) > 48 * 3600:
                        cs['value'] += 1
                        csqt["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsqt["value"] += 1

        # zdallalertcount = getyzend(4)
        # yzallalertcount = getyzend(3)
        # zdcsalert = getcs(4)
        # yzcsalert = getcs(3)

        alertlevcount = {"alertzd": alertzd, "alertyz": alertyz, "alertyb": alertyb, "alertqt": alertqt,
                         "alertlist": alertlist, "zdlist": zdlist, "yzlist": yzlist, "yblist": yblist,
                         "qtlist": qtlist, "cs": cs, "wcs": wcs,"wcszd": wcszd, "wcsyz": wcsyz, "wcsyb": wcsyb,
                         "wcsqt": wcsqt, "cszd": cszd, "csyz": csyz, "csyb": csyb, "csqt": csqt, "zdapplist": zdapplist,
                         "yzapplist": yzapplist, "ybapplist": ybapplist, "qtapplist": qtapplist
                        }
        return alertlevcount


# 表盘
def headbp(user, timedur):
    if int(timedur) == 0:
        zdallalertcount = getyzend(user, 4, timedur)
        yzallalertcount = getyzend(user, 3, timedur)
        zdcsalert = getcs(user, 4, timedur)
        yzcsalert = getcs(user, 3, timedur)
        data = {"zdallalertcount": zdallalertcount, "yzallalertcount": yzallalertcount,
                "zdcsalert": zdcsalert, "yzcsalert": yzcsalert}
    else:
        zdallalertcount = getyzend(user, 4, timedur)
        yzallalertcount = getyzend(user, 3, timedur)
        zdcsalert = getcs(user, 4, timedur)
        yzcsalert = getcs(user, 3, timedur)
        data = {"zdallalertcount2": zdallalertcount, "yzallalertcount2": yzallalertcount,
                "zdcsalert2": zdcsalert, "yzcsalert2": yzcsalert}

    return data


# 在处理告警
def dealalarm(request):
    iplist = get_ip_list(request.user)

    alertlist = []
    #alerts = Jk_alert.objects.filter(Type_ip__in=iplist).filter(A_time__isnull=False) # 修改
    alerts = Alert.objects.filter(ip__in=iplist).filter(ack_time__isnull=False)
    pageIndex = int(request.GET.get('page', ''))
    pageSize = int(request.GET.get('limit', ''))
    count = 0
    total = len(alerts)

    for i in alerts[(pageIndex-1)*pageSize:pageIndex*pageSize]:

            if i.status == 0:
                status = "解决"
            else:
                status = "未解决"

            if i.ack_time:
                atime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.ack_time)))
            else:
                atime = ""
            host = None
            Application = None
            if i.device_type == "物理机":

                hostnames = ServerToZabbix.objects.filter(host_ip=i.ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.device_type == "宿主机":
                hostnames = ResourceHostToZabbix.objects.filter(host_ip=i.ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.device_type == "云主机":
                hostnames = CloudDeviceToZabbix.objects.filter(host_ip=i.ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.device_type == "网络交换机" or i.device_type == "负载均衡" or i.device_type == "防火墙":
                hostnames = NetworkDeviceToZabbix.objects.filter(host_ip=i.ip)
                for h in hostnames:
                    host = h.hostname

            alertlist.append({"eventid": i.eventid, "Alert_lev_id": i.lev.name, 'ip': i.ip, "Application": Application,
                              "Type": i.device_type, "hostname": host, "message": i.message,
                              "Oc_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.oc_time))),
                              "A_time": atime,
                              "Sendto": i.sendto, "Status": status, "item": i.item})
            count += 1

    alertjson = {"code": 0, "msg": "", "count": total, "data": alertlist}
    return HttpResponse(json.dumps(alertjson))


# 告警数量
def getcount(type, iplist, lev):
    conutlist = []
    for i in type:
        # print(i)
        #conutlist.append(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Type=i).filter(Alert_lev_id_id=lev).count()) # 修改
        conutlist.append(Alert.objects.filter(ip__in=iplist).filter(device_type=i).filter(lev_id=lev).count())
        # print(conutlist)
    return conutlist


# 服务器告警
def serveralarm(user):

    iplist = get_ip_list(user)
    type = ["物理机", "宿主机", "云主机"]
    zdlist = getcount(type, iplist, 4)
    yzlist = getcount(type, iplist, 3)
    yblist = getcount(type, iplist, 2)
    qtlist = getcount(type, iplist, 1)
    content = {"zd": zdlist, "yz": yzlist, "yb": yblist, "qt": qtlist}
    return content


# 网络设备告警、
def networkalarm(user):

    iplist = get_ip_list(user)
    type = ["交换机", "路由器", "防火墙", "负载均衡"]
    zdlist = getcount(type, iplist, 4)
    yzlist = getcount(type, iplist, 3)
    yblist = getcount(type, iplist, 2)
    qtlist = getcount(type, iplist, 1)
    content = {"zdn": zdlist, "yzn": yzlist, "ybn": yblist, "qtn":qtlist}
    return content


# 签退信息
def maintaininfo(request):
    pageIndex = int(request.GET.get('page', ''))
    pageSize = int(request.GET.get('limit', ''))
    now = time.time()
    iplist = get_ip_list(request.user)
    #allinfo = Jk_Mt_Information.objects.filter(IP__in=iplist).filter(Q(Oc_time__lte=now),Q(End_time__gte=now)) # 修改
    allinfo = MTInformation.objects.filter(ip__in=iplist).filter(Q(oc_time__lte=now), Q(end_time__gte=now))
    infolist = []
    count = 0
    total = len(allinfo)
    for info in allinfo[(pageIndex - 1) * pageSize:pageIndex * pageSize]:

        # if info.Oc_time <= now and info.End_time >=now:
            infolist.append({"name": info.Name, "ip": info.ip,
                             "Oc_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info.oc_time))),
                             "End_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info.end_time)))})
            # print(infolist)
            count += 1
    content = {"code": 0, "msg": "", "count": total, "data": infolist}
    return HttpResponse(json.dumps(content))


# 仪表盘
# @login_required
def dashBoard(request):
    if request.method == 'GET':

        ztalarms = ztalarmEvent(request.user)
        salarm = serveralarm(request.user)
        nalarm = networkalarm(request.user)
        halarm1 = headbp(request.user, 0)
        halarm2 = headbp(request.user, 1)
        atalarm = dict(salarm, **ztalarms)
        headalarm = dict(atalarm, **nalarm)
        headalarm2 = dict(headalarm, **halarm1)
        ztalarm = dict(headalarm2, **halarm2)
        return render(request, 'dashBoard/dashboard.html', ztalarm)

    elif request.method == 'POST':
        # timedur = request.POST.get("timedur", '')
        # if timedur:
        #     ztalarms = ztalarmEvent()
        #     salarm = serveralarm()
        #     nalarm = networkalarm()
        #     halarm = headbp()
        #     atalarm = dict(salarm, **ztalarms)
        #     headalarm = dict(atalarm, **nalarm)
        #     ztalarm = dict(headalarm, **halarm)
        #
        #     return render(request, 'dashBoard/dashboard.html', ztalarm)

        pass
