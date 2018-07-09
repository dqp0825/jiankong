# coding:utf-8
import logging
import time
import json
import requests


from django.db.models import Q
from django.shortcuts import render,HttpResponse

from dashBoard.models import ServerToZabbix,CloudDeviceToZabbix,ResourceHostToZabbix,StorageToZabbix
# from dashBoard.models import Jk_alert_lev,Jk_alert,Jk_Device_Type,Jk_Alert_His,Jk_Fault,NetworkDeviceToZabbix
# 修改 Jk_alert_lev：告警级别表 Jk_alert：告警信息表 Jk_Device_Type：设备类型表
# Jk_Alert_His：告警信息历史表  Jk_Fault：故障等级时限表Jk_Fault NetworkDeviceToZabbix：网络设备
from dashBoard.models import AlertLev,Alert,DeviceType,AlertHis,Fault,NetworkDeviceToZabbix

# from dashBoard.models import Jk_Mt_Information,Jk_App
# 修改  Jk_Mt_Information:维护状态表  Jk_App:应用表
# from dashBoard.models import MTInformation,App

from django.contrib.auth.decorators import login_required





from signbackInformation.views import  get_ip_list
# Create your views here.
# logger = logging.getLogger("tofile")


from django import forms

class UserForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)


# user = "Admin"

#首页
# @login_required
def index(request):

    url = "http://10.192.200.32/zabbix/api_jsonrpc.php"
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
    except:
        auth = ''
    return render(request, "myindex.html", {"auth": auth})

#登录
# @csrf_exempt
# def login(request):
#     context = {}
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             # 获取表单用户密码
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             # 获取的表单数据与数据库进行比较
#             user = authenticate(username=username, password=password)
#             if user:
#                 # 比较成功，跳转index
#                 auth.login(request, user)
#                 request.session['username'] = username
#                 return redirect('/index/')
#             else:
#                 # 比较失败，还在login
#                 context = {'isLogin': False, 'pawd': False}
#                 return render(request, 'login.html', context)
#     else:
#         context = {'isLogin': False, 'pswd': True}
#     return render(request, 'login.html', context)
#     pass



#获取用户的资源
def getips(user):
    serverip = ServerToZabbix.objects.filter(user=user)
    cloudip = CloudDeviceToZabbix.objects.filter(user=user)
    resourceip = ResourceHostToZabbix.objects.filter(user=user)
    storageip = StorageToZabbix.objects.filter(user=user)
    networkip = NetworkDeviceToZabbix.objects.filter(user=user)
    iplist = []
    for server in serverip:
        iplist.append((server.host_ip).replace('\t',''))
    for cloud in cloudip:
        iplist.append((cloud.host_ip).replace('\t',''))
    for storage in storageip:
        iplist.append((storage.host_ip).replace('\t',''))
    for network in networkip:
        iplist.append((network.host_ip).replace('\t',''))
    for resource in resourceip:
        iplist.append((resource.host_ip).replace('\t',''))
    return iplist


#告警完成数
def getyzend(user, lev, timedur):
    if int(timedur) == 0:
        timedur = time.time() - 7*24*3600
    else:
        timedur = time.time() - 30*24*3600
    iplist =  get_ip_list(user)
    # iplist = getips(user)
    # allalerthis = Jk_Alert_His.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=int(lev)).filter(End_time__gt=timedur).count() # 修改
    allalerthis = AlertHis.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=int(lev)).filter(End_time__gt=timedur).count()
    return allalerthis


#告警超时数
def getcs(user, lev, timedur):
    iplist =  get_ip_list(user)
    starttime = time.time()
    if int(timedur) == 0:
        timedur = time.time() - 7*24*3600
    else:
        timedur = time.time() - 30*24*3600
    # alertcs = Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)        #当前告警超时 修改
    alertcs = Alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)        #当前告警超时
    alerthiscs = AlertHis.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=lev).filter(Oc_time__gt=timedur)   #历史告警超时
    count = 0

    for alert in alertcs:
        # if starttime - alert.Oc_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600:  # 修改
        if starttime - alert.Oc_time > int(Fault.objects.get(Fault_id=lev).DESC) * 3600:  # 修改
            count += 1
    for alerthis in alerthiscs:
        # if alerthis.End_time - alerthis.Oc_time > int(Jk_Fault.objects.get(Fault_id=lev).DESC) * 3600: # 修改
        if alerthis.End_time - alerthis.Oc_time > int(Fault.objects.get(Fault_id=lev).DESC) * 3600:
            count += 1

    return count

#整体告警
def ztalarmEvent(user):
    # if request.method == 'GET':
        alertlist = []
        alertzd = 0
        alertyz = 0
        alertyb = 0
        alertqt = 0
        iplist =  get_ip_list(user)
        typelist = []
        alerts = Jk_alert.objects.all()
        types = Jk_Device_Type.objects.all()
        TypeList = []
        for type in types:
            TypeList.append(type.TypeName)
        #告警设备类型
        zdlist = []
        yzlist = []
        yblist = []
        qtlist = []
        AppList = []
        #告警设备App
        # apps = Jk_App.objects.all() # 修改
        apps = App.objects.all()


        for app in apps:
            AppList.append(app.AppName)
        zdapplist = []
        yzapplist = []
        ybapplist = []
        qtapplist = []
    #设备类型告警
        for i in TypeList:

            zdlist.append({"value":Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=4).count(),
                           "name":str(i)+":"+str(Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=4).count())})

            yzlist.append({"value": Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=3).count(),
                           "name": str(i)+":"+str(Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=3).count())})

            yblist.append({"value": Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=2).count(),
                           "name": str(i)+":"+str(Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=2).count())})

            qtlist.append({"value": Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=1).count(),
                           "name": str(i)+":"+str(Jk_alert.objects.filter(Type=i).filter(
                Type_ip__in=iplist).filter(Alert_lev_id_id=1).count())})


        # for i in alerts:
        #     # zd = {"value": 0, "name": ""}
        #     if (i.Type_ip).strip() in iplist:
        #         zdlist.append({"value": Jk_alert.objects.filter(Type=i).filter(
        #             Type_ip__in=iplist).filter(Alert_lev_id_id=4).count(), "name": i})

        #应用告警
        for j in AppList:

            zdapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4).count(),
                              "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=4).count())})

            yzapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3).count(),
                              "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=3).count())})

            ybapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2).count(),
                              "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=2).count())})

            qtapplist.append({"value": Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1).count(),
                              "name": str(j)+":"+str(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Alert_lev_id_id=1).count())})

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
        cslist = []
        wcslist = []
        for j in alerts:
            ctime = time.time()

            if (j.Type_ip).strip() in iplist:
                if (j.Alert_lev_id).Alert_lev_id == 1:
                    if int(ctime) - int(j.Oc_time) > 2 * 3600:
                        cs['value'] += 1
                        cszd["value"] +=1
                    else:
                        wcs['value'] += 1
                        wcszd["value"]+=1

                if (j.Alert_lev_id).Alert_lev_id == 2:
                    if int(ctime) - int(j.Oc_time) > 4 * 3600:
                        cs['value'] += 1
                        csyz["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyz["value"] += 1

                if (j.Alert_lev_id).Alert_lev_id == 3:
                    if int(ctime) - int(j.Oc_time) > 8 * 3600:
                        cs['value'] += 1
                        csyb["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyb["value"] += 1

                if (j.Alert_lev_id).Alert_lev_id == 4:
                    if int(ctime) - int(j.Oc_time) > 48 * 3600:
                        cs['value'] += 1
                        csqt["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsqt["value"] += 1

        # zdallalertcount = getyzend(4)
        # yzallalertcount = getyzend(3)
        # zdcsalert = getcs(4)
        # yzcsalert = getcs(3)

        alertlevcount = {"alertzd":alertzd, "alertyz": alertyz, "alertyb": alertyb, "alertqt": alertqt,
                         "alertlist": alertlist, "zdlist": zdlist, "yzlist": yzlist, "yblist": yblist,
                         "qtlist": qtlist, "cs": cs, "wcs": wcs,"wcszd": wcszd, "wcsyz": wcsyz, "wcsyb": wcsyb,
                         "wcsqt": wcsqt, "cszd": cszd, "csyz": csyz, "csyb": csyb, "csqt": csqt, "zdapplist": zdapplist,
                         "yzapplist": yzapplist, "ybapplist": ybapplist, "qtapplist": qtapplist
                        }
        return alertlevcount


#表盘
def headbp(user, timedur):
    if int(timedur)== 0:
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



#在处理告警
def dealalarm(request):
    iplist =  get_ip_list(request.user)
    # print(iplist)
    alertlist = []
    #alerts = Jk_alert.objects.filter(Type_ip__in=iplist).filter(A_time__isnull=False) # 修改
    alerts = Alert.objects.filter(Type_ip__in=iplist).filter(A_time__isnull=False)
    pageIndex = int(request.GET.get('page', ''))
    pageSize = int(request.GET.get('limit', ''))
    count = 0
    total = len(alerts)
    # print(total)
    for i in alerts[(pageIndex-1)*pageSize:pageIndex*pageSize]:

            if i.Status == 0:
                status = "解决"
            else:
                status = "未解决"

            if i.A_time:
                atime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.A_time)))
            else:
                atime = ""
            host = None
            Application = None
            if i.Type == "物理机":
                # print(i.Type_ip)
                hostnames = ServerToZabbix.objects.filter(host_ip=i.Type_ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.Type == "宿主机":
                hostnames = ResourceHostToZabbix.objects.filter(host_ip=i.Type_ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.Type == "云主机":
                hostnames = CloudDeviceToZabbix.objects.filter(host_ip=i.Type_ip)
                for h in hostnames:
                    host = h.hostname
                    Application = h.app_name
            elif i.Type == "网络交换机" or i.Type == "负载均衡" or i.Type == "防火墙":
                hostnames = NetworkDeviceToZabbix.objects.filter(host_ip=i.Type_ip)
                for h in hostnames:
                    host = h.hostname


            alertlist.append({"eventid":i.eventid,"Alert_lev_id":(i.Alert_lev_id).LevName,'ip':i.Type_ip,"Application":Application,
                              "Type":i.Type,"hostname":host,"message":i.message,
                              "Oc_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.Oc_time))),
                              "A_time":atime,
                              "Sendto":i.Sendto,"Status":status,"item":i.item})
            count += 1
    # print(alertlist)
    alertjson = {"code": 0, "msg": "", "count": total, "data":alertlist}
    return HttpResponse(json.dumps(alertjson))


#应用告警


#告警数量
def getcount(type,iplist,lev):
    conutlist = []
    for i in type:
        # print(i)
        #conutlist.append(Jk_alert.objects.filter(Type_ip__in=iplist).filter(Type=i).filter(Alert_lev_id_id=lev).count()) # 修改
        conutlist.append(Alert.objects.filter(Type_ip__in=iplist).filter(Type=i).filter(Alert_lev_id_id=lev).count())
        # print(conutlist)
    return conutlist


#服务器告警
def serveralarm(user):

    iplist =  get_ip_list(user)
    type = ["物理机", "宿主机", "云主机"]
    zdlist = getcount(type, iplist, 4)
    yzlist = getcount(type, iplist, 3)
    yblist = getcount(type, iplist, 2)
    qtlist = getcount(type, iplist, 1)
    content = {"zd":zdlist, "yz":yzlist, "yb":yblist, "qt":qtlist}
    return content


#网络设备告警、
def networkalarm(user):

    iplist =  get_ip_list(user)
    type = ["交换机", "路由器", "防火墙", "负载均衡"]
    zdlist = getcount(type, iplist, 4)
    yzlist = getcount(type, iplist, 3)
    yblist = getcount(type, iplist, 2)
    qtlist = getcount(type, iplist, 1)
    content = {"zdn":zdlist, "yzn":yzlist, "ybn":yblist, "qtn":qtlist}
    return content




##签退信息
def maintaininfo(request):
    pageIndex = int(request.GET.get('page', ''))
    pageSize = int(request.GET.get('limit', ''))
    now = time.time()
    iplist =  get_ip_list(request.user)
    #allinfo = Jk_Mt_Information.objects.filter(IP__in=iplist).filter(Q(Oc_time__lte=now),Q(End_time__gte=now)) # 修改
    allinfo = MTInformation.objects.filter(IP__in=iplist).filter(Q(Oc_time__lte=now),Q(End_time__gte=now))
    infolist = []
    count = 0
    total = len(allinfo)
    for info in allinfo[(pageIndex - 1) * pageSize:pageIndex * pageSize]:

        # if info.Oc_time <= now and info.End_time >=now:
            infolist.append({"name":info.Name,"ip":info.IP,
                             "Oc_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info.Oc_time))),
                             "End_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(info.End_time)))})
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

        return render(request,'dashBoard/dashboard.html', ztalarm)

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
