# coding:utf-8
import json
import time
import uuid
import xlwt
from io import StringIO, BytesIO

from django.urls import reverse_lazy
from django.http import JsonResponse, StreamingHttpResponse
from django.core.cache import cache
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from dashBoard.models import ServerToZabbix, CloudDeviceToZabbix
from dashBoard.models import ResourceHostToZabbix, StorageToZabbix, NetworkDeviceToZabbix
# from dashBoard.models import Jk_alert, Jk_App, Jk_alert_lev, Jk_Fault, Jk_Device_Type, Jk_Server, JK_Shebei_Group, \
#     Jk_Alert_His, Jk_pass

# 修改
from dashBoard.models import Alert,AlertLev,Fault,DeviceType,Server,DeviceGroup,AlertHis,ZabbixPass

# from dashBoard.models import ServerToZabbix, CloudDeviceToZabbix, ResourceHostToZabbix, StorageToZabbix

# 修改
from dashBoard.models import ServerToZabbix,CloudDeviceToZabbix,ResourceHostToZabbix,StorageToZabbix

# from dashBoard.models import (Jk_Resource_Host, Jk_Server, Jk_Cloud_Device, Jk_Storage, Jk_Switches,
#                               Jk_Routing, Jk_Fw, Jk_Fz)
# 修改
from dashBoard.models import ResourceHost,Server,CloudDevice,Storage,Switches,Routing,Fw,Fz


from dashBoard.models import NetworkDeviceToZabbix
from signbackInformation.views import get_zabbix_token, to_strtime, to_localtime, get_sign_out , get_ip_list

# Create your views here.


user = "admin"

# 整体的进行修改
def get_hostid(shebei_type, ip, name):
    if shebei_type == "物理机":
        server_host = Server.objects.filter(ip=ip, name=name)
        # return Server.objects.filter(ip=ip, name=name).hostid
        return '无数据' if not server_host else server_host[0]
    elif shebei_type == "宿主机":
        resource_host = ResourceHost.objects.get(ip=ip, name=name).hostid
        # return ResourceHost.objects.get(ip=ip, name=name).hostid
        return '无数据' if not resource_host else resource_host[0]
    elif shebei_type == "云主机":
        cloud_device = CloudDevice.objects.get(ip=ip, name=name).hostid
            # return CloudDevice.objects.get(ip=ip, name=name).hostid
        return '无数据' if not cloud_device else cloud_device[0]
    elif shebei_type == "存储":
        storage = Storage.objects.get(ip=ip, name=name).hostid[0]
        return '无数据' if not storage else storage[0]
    elif shebei_type == "交换机":
            return Switches.objects.get(ip=ip, name=name).hostid
    elif shebei_type == "路由器":
            return Routing.objects.get(ip=ip, name=name).hostid
    elif shebei_type == "防火墙":
            return Fw.objects.get(ip=ip, name=name).hostid
    elif shebei_type == "负载均衡":
            return Fz.objects.get(ip=ip, name=name).hostid


def get_sendto(A_time):
        '''伪造受理人'''
        if A_time:
            return 'admin'
        else:
            return ''


def get_status(Status):
    if Status:
        return '已受理'
    else:
        return '未受理'


# def to_strtime(datatime):
#     try:
#         return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datatime)))
#     except TypeError:
#         return datatime


#获取告警信息
def getalarm(request):
    # iplist = getips(user)
    iplist = get_ip_list(request.user)
    alertlist = []
    # alerts = Jk_alert.objects.all()  # 修改
    alerts = Alert.objects.all()
    print(alerts)
    # print("alerts")
    count = 0
    for i in alerts:
        # print(i.ip)
        # print(i.status)
        # print(i.device_type)
        # 根据报错信息将ip进行修改 修改为ip
        if (i.ip).strip() in iplist:

            if i.status == 0:
                status = "解决"
            else:
                status = "未解决"

            if i.ack_time:
                atime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.ack_time)))
            else:
                atime = ""

            if i.device_type == "物理机":
                hostnames = ServerToZabbix.objects.filter(host_ip=i.ip)
                for h in hostnames:
                    hostname = h
            elif i.device_type == "宿主机":
                hostnames = ResourceHostToZabbix.objects.filter(host_ip=i.ip)[0].hostname
                for h in hostnames:
                    hostname = h
            elif i.device_type == "云主机":
                hostnames = CloudDeviceToZabbix.objects.filter(host_ip=i.ip)[0].hostname
                for h in hostnames:
                    hostname = h
            elif i.device_type == "网络交换机" or i.device_type == "负载均衡" or i.device_type == "防火墙":
                hostnames = NetworkDeviceToZabbix.objects.filter(host_ip=i.ip)[0].hostname
                for h in hostnames:
                    hostname = h
            # alertlist.append({"Alert_lev_id":(i.lev_id).name,"Application":"Ucloud_Paas",
            alertlist.append({"Alert_lev_id":(i.lev_id),"Application":"Ucloud_Paas",
                              "Type":i.device_type,"hostname":hostname,"message":i.message,
                              "Oc_time":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.oc_time))),
                              "A_time":atime,
                              "Sendto":i.sendto,"Status":status,"item":i.item})
            count += 1
    alertjson = {"code": 0, "msg": "", "count": count, "data":alertlist}
    print(alertlist)
    print("eeeeeeeeeeeeeee")
    print(json.dumps(alertjson))

    return HttpResponse(json.dumps(alertjson),content_type='application/json')


# 告警
@csrf_exempt
def alarmEvent(request):
    if request.method == 'GET':
        alertlist = []
        alertzd = 0
        alertyz = 0
        alertyb = 0
        alertqt = 0
        # iplist = getips(user)
        iplist = get_ip_list(request.user)
        typelist = []



        # alerts = Jk_alert.objects.all() # 修改
        alerts = Alert.objects.all()

        # types = Jk_Device_Type.objects.all() # 修改
        types = DeviceType.objects.all()
        TypeList = []
        for type in types:
            TypeList.append(type.name)
        zdlist = []
        yzlist = []
        yblist = []
        qtlist = []
        for i in TypeList:

            # zdlist.append({"value":Jk_alert.objects.filter(Type=i).filter( # 修改
            zdlist.append({"value":Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(lev_id=4).count(),"name":i})

            # yzlist.append({"value": Jk_alert.objects.filter(Type=i).filter(  # 修改
            yzlist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(lev_id=3).count(), "name": i})

            # yblist.append({"value": Jk_alert.objects.filter(Type=i).filter(  # 修改
            yblist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(lev_id=2).count(), "name": i})

            # qtlist.append({"value": Jk_alert.objects.filter(Type=i).filter(  # 修改
            qtlist.append({"value": Alert.objects.filter(device_type=i).filter(
                ip__in=iplist).filter(lev_id=1).count(), "name": i})


        #告警分类
        for i in alerts:
            zd = {"value": 0, "name": ""}
            if (i.ip).strip() in iplist:
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

            if (j.ip).strip() in iplist:
                # if (j.lev_id).lev_id == 1:
                if (j.lev_id) == 1:
                    # cshour = Jk_Fault.objects.filter(Fault_name=((j.Alert_lev_id).LevName))[0].DESC
                    if int(ctime) - int(j.oc_time) > 2 * 3600:
                        cs['value'] += 1
                        cszd["value"] +=1
                    else:
                        wcs['value'] += 1
                        wcszd["value"]+=1

                # if (j.lev_id).lev_id == 2:
                if (j.lev_id) == 2:
                    # cshour = Jk_Fault.objects.filter(Fault_name=((j.Alert_lev_id).LevName))[0].DESC
                    if int(ctime) - int(j.oc_time) > 4 * 3600:
                        cs['value'] += 1
                        csyz["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyz["value"] += 1

                if (j.lev_id) == 3:
                    # cshour = Jk_Fault.objects.filter(Fault_name=(j.Alert_lev_id).LevName)[0].DESC
                    if int(ctime) - int(j.oc_time) > 8 * 3600:
                        cs['value'] += 1
                        csyb["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsyb["value"] += 1

                if (j.lev_id) == 4:
                    # cshour = Jk_Fault.objects.filter(Fault_name=(j.Alert_lev_id).LevName)[0].DESC
                    if int(ctime) - int(j.oc_time) > 48 * 3600:
                        cs['value'] += 1
                        csqt["value"] += 1
                    else:
                        wcs['value'] += 1
                        wcsqt["value"] += 1

        # Device_Type_list = Jk_Device_Type.objects.all()  # 修改
        Device_Type_list = DeviceType.objects.all()
        # alert_lev_list = Jk_alert_lev.objects.all()  # 修改
        alert_lev_list = AlertLev.objects.all()  # 修改

        ip = request.GET.get('ip', '')

        if ip:
            ip = ip
        else:
            ip = ''
        alertlevcount = {"alertzd": alertzd, "alertyz": alertyz, "alertyb": alertyb, "alertqt": alertqt,
                         "alertlist": alertlist, "zdlist": zdlist, "yzlist": yzlist, "yblist": yblist,
                         "qtlist": qtlist, "cs": cs, "wcs": wcs, "wcszd": wcszd, "wcsyz": wcsyz, "wcsyb": wcsyb,
                         "wcsqt": wcsqt, "cszd": cszd, "csyz": csyz, "csyb": csyb, "csqt": csqt,
                         'Device_Type_list': Device_Type_list, 'alert_lev_list': alert_lev_list,'ip': ip}

        return render(request, 'alarmEvents/alarmEvent.html', alertlevcount)
    elif request.method == 'POST':
        """加载列表搜索"""
        # iplist = getips(user)
        machine = request.POST.get('machine', '')  # 告警内容
        appname = request.POST.get('appname', '')
        hostname = request.POST.get('hostname', '')
        ip = request.POST.get('ip', '')
        Device_Type = request.POST.get('Device_Type', '')
        alert_lev = request.POST.get('alert_lev', 0) # 告警等级
        pageIndex = int(request.POST.get('page', 1))
        pageSize = int(request.POST.get('limit', 10))
        iplist = get_ip_list(request.user, appname)

        # alert_list = Jk_alert.objects.filter(ip__in=iplist) # 修改
        alert_list = Alert.objects.filter(ip__in=iplist)
        # print("****alert_list******")
        # print(alert_list)
        # print("****alert_list******")
        # if alert_lev and Device_Type:
        #     print("sssssss",DeviceType)
        #     alert_list = alert_list.filter(lev_id=alert_lev, device_type=Device_Type)
        # elif alert_lev:
        #     alert_list = alert_list.filter(lev_id=alert_lev)
        # elif Device_Type:
        #     alert_list = alert_list.filter(device_type=Device_Type)
        #
        # if hostname:
        #     alert_list = alert_list.filter(device_name=hostname)
        # if ip:
        #     alert_list = alert_list.filter(ip=ip)
        # if machine:
        #     # alert_list = alert_list.filter(message__icontains=machine)
        #     alert_list = alert_list.filter(message=machine)
        # alert_list = alert_list.order_by('-lev_id')
        res = []

        # 表格的字段： 级别，所属应用，告警设备，告警内容，发生时间，受理时间，受理人，解决，功能
        for p in alert_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]: # alert_list:是Alert的属性

            try:
                print(get_hostid(p.device_type, p.ip, p.device_name))
            except Exception as e:
                print(e)
            print(get_sign_out(p.ip))
            print("*******pppp*******")
            res.append({
                # "Alert_id": p.Alert_id, "Alert_lev_id": p.Alert_lev_id.LevName, "Application": iplist[p.ip], 'request_user': 'admin',
                "Alert_id": p.id, "Alert_lev_id": p.lev.name, "Application": iplist[p.ip], 'request_user': 'admin',

                # "Typename": p.Typename, "ip": p.ip, "message": p.message, "item": p.item,
                "Typename": p.device_type, "ip": p.ip, "message": p.message, "item": p.item,

                # "Oc_time": to_strtime(p.Oc_time), "A_time": to_strtime(p.A_time), "Sendto": get_sendto(p.A_time), "eventid": p.eventid,
                "Oc_time": to_strtime(p.oc_time), "A_time": to_strtime(p.ack_time), "Sendto": get_sendto(p.ack_time), "eventid": p.eventid,
                # "Status": get_status(p.Status), "DESC": p.DESC, "zabbix_id": p.zabbix_id, "hostid": get_hostid(p.Type, p.ip, p.Typename),
                "Status": get_status(p.status), "DESC": p.desc, "zabbix_id": p.zabbix_id, "hostid": get_hostid(p.device_type, p.ip, p.device_name),
                "sign_out": get_sign_out(p.ip)})

        res_content = {
            "code": 0,
            "msg": "",
            "count": len(alert_list),
            "data": res
        }
        print(res_content)
        return HttpResponse(json.dumps(res_content), content_type='application/json')


# 历史告警
@csrf_exempt
def alarm_his(request):
    if request.method == 'GET':
        # Device_Type_list = Jk_Device_Type.objects.all() #  修改
        Device_Type_list = DeviceType.objects.all()  # 设备类型表
        # alert_lev_list = Jk_alert_lev.objects.all() # 修改
        alert_lev_list = AlertLev.objects.all() # 告警等级表
        alertlevcount = {'Device_Type_list': Device_Type_list, 'alert_lev_list': alert_lev_list}
        return render(request, 'alarmEvents/alarm_his.html', alertlevcount)
    if request.method == 'POST':
        print("zouwo")
        machine = request.POST.get('machine', '')
        appname = request.POST.get('appname', '')
        hostname = request.POST.get('hostname', '')
        ip = request.POST.get('ip', '')
        Device_Type = request.POST.get('Device_Type', '')
        alert_lev = request.POST.get('alert_lev', 0)
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')
        pageIndex = int(request.POST.get('page', 1))
        pageSize = int(request.POST.get('limit', 10))
        iplist = get_ip_list(request.user, appname)
        print("iplist",iplist)
        #alert_list = Jk_Alert_His.objects.filter(ip__in=iplist) # 修改
        alert_list = AlertHis.objects.filter(ip__in=iplist) # 修改
        print("alert_list:",alert_list)
        if alert_lev:
            alert_list = alert_list.filter(lev=alert_lev)
        if Device_Type:
            alert_list = alert_list.filter(device_type=Device_Type)

        if startTime and endTime:
            alert_list = alert_list.filter(
                Q(end_time__lt=to_localtime(str(endTime)), end_time__gt=to_localtime(str(startTime))) |
                Q(oc_time__lt=to_localtime(str(endTime)), oc_time__gt=to_localtime(str(startTime)))

            )
        elif not startTime and endTime:
            alert_list = alert_list.filter(
                Q(end_time__lt=to_localtime(str(endTime))) |
                Q(oc_time__lt=to_localtime(str(endTime)))
            )
        elif not endTime and startTime:
            alert_list = alert_list.filter(
                Q(end_time__gt=to_localtime(str(startTime))) |
                Q(oc_time__gt=to_localtime(str(startTime)))
            )
        # else:
        #     localtime = time.time() - 60 * 60 * 24 * 7
        #     alert_list = alert_list.filter(
        #         Q(End_time__gt=localtime) |
        #         Q(Oc_time__gt=localtime)
        #     )
        if hostname:
            alert_list = alert_list.filter(device_name__icontains=hostname)
        if ip:
            alert_list = alert_list.filter(ip__icontains=ip)
        if machine:
            alert_list = alert_list.filter(item__icontains=machine)

        # alert_list = alert_list.order_by('-Alert_lev_id')
        res = []
        for p in alert_list[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            print("*****xxxxxxx******")
            print(p.id)
            print("*****xxxxxx******")
            res.append({
                "Alert_His_id": p.id, "Alert_lev_id": p.lev.name, "Application": iplist[p.ip],
                "state": '已解决', "ip": p.ip, "message": p.message, "item": p.item,
                "Oc_time": to_strtime(p.oc_time, ), "End_time": to_strtime(p.end_time), "A_time": to_strtime(p.A_time),
                "Sendto": get_sendto(p.a_time), "Status": get_status(p.a_time), "DESC": p.desc, "Typename": p.device_name,
                "Deal_Person": p.deal_person, "Deal_Details": p.deal_details, "Deal_End_time": p.deal_end_time
            })
        res_content = {
            "code": 0,
            "msg": "",
            "count": len(alert_list),
            "data": res
        }
        return HttpResponse(json.dumps(res_content), content_type='application/json')


# 受理
def host_acknowledge(request):
    if request.method == 'GET':
        message = request.GET.get('message', '已受理') or '已受理'
        message = '{}:{}'.format(request.user.username, message)
        eventids = request.GET.get('eventids', '')
        zabbix_id = request.GET.get('zabbix_id', 0)
        zapi = get_zabbix_token(zabbix_id)
        if type(eventids) is not list:
            eventids = [eventids, ]
        res = zapi.event.acknowledge(eventids=eventids, message=message)
        return HttpResponse(json.dumps(res), content_type='application/json')


# 导出当前告警
@csrf_exempt
def alarmEvents_export(request):
    if request.method == 'GET':
        # 表头预处理
        fields = [
            field for field in Jk_alert._meta.fields
            if field.name not in [
                'eventid', 'zabbix_id', 'Status', 'Alert_id'
            ]
        ]
        # 表名
        filename = '{}-alarm.xls'.format(
            time.strftime("%Y-%m-%d", time.localtime(time.time()))
        )

        def _map_header(field_name):
            header_dic = {
            'Alert_id': '告警信息ID',
            'Alert_lev_id': '告警级别',
            'Application': '所属应用',
            'item': '监控项',
            'Type': '设备类型',
            'Typename': '设备名',
            'ip': '设备IP',
            'message': '告警内容',
            'Oc_time': '发生时间',
            'A_time': '受理时间',
            'Sendto': '受理人',
            'Status': '受理结果',
            'DESC': '描述'
            }
            return header_dic[field_name]
        header = [_map_header(str(field.name)) for field in fields]
        spm = request.GET.get('spm', '')  # <QueryDict: {'spm': ['6d48f7c0559242569fc6df8198fbfa26']}>
        if spm:
            alert_list = cache.get(spm)
        # 写入excel
        wb = xlwt.Workbook(encoding='utf-8')
        sheet_1 = wb.add_sheet(u'当前告警')
        for i in range(len(header)):
            sheet_1.write(0, i, header[i])

        ip_list = get_ip_list(request.user)
        for index, alert in enumerate(alert_list):
            if isinstance(alert, Jk_alert):
                AppName = ip_list[alert.ip]
                data = [getattr(alert, field.name) for field in fields]
                for i in range(len(data)):
                    if str(data[i]) == 'None':
                        sheet_1.write(index + 1, i, '')
                    elif str(fields[i].name) == 'Application':
                        sheet_1.write(index + 1, i, AppName)
                    elif str(fields[i].name) == 'Oc_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'A_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'Alert_lev_id':
                        sheet_1.write(index + 1, i, data[i].LevName)
                    elif str(fields[i].name) == 'Sendto':
                        if str(data[i]) == '':
                            sheet_1.write(index + 1, i, '')
                        else:
                            sheet_1.write(index + 1, i, 'admin')
                    else:
                        sheet_1.write(index + 1, i, str(data[i]))
            else:
                continue
        #
        # # 将生成的excel放入byte流给response
        bio = BytesIO()
        wb.save(bio)
        bio.seek(0)

        response = StreamingHttpResponse(bio)  # 直接读bio就可以，不用bio.getvalue()!!!!! 用二进制文件方式读取
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        return response #HttpResponse(','.join([field.name for field in fields]))

    elif request.method == 'POST':
        try:
            alerts = json.loads(request.body)
        except ValueError:
            return HttpResponse('Json object not valid', status=400)
        alerts_id =alerts.get('alerts_id', [])
        appname = request.POST.get('appname', '')
        machine =alerts.get('machine', '')
        hostname = alerts.get('hostname', '')
        ip = alerts.get('ip', '')
        Device_Type = alerts.get('Device_Type', '')
        alert_lev = alerts.get('alert_lev', 0)

        if alerts_id:
            # alert_list = Jk_alert.objects.filter(Alert_id__in=alerts_id) # 修改
            alert_list = Alert.objects.filter(Alert_id__in=alerts_id)
        else:
            iplist = get_ip_list(request.user, appname)
            # alert_list = Jk_Alert_His.objects.filter(ip__in=iplist) # 修改
            alert_list = AlertHis.objects.filter(ip__in=iplist)
            if alert_lev:
                alert_list = alert_list.filter(Alert_lev_id=alert_lev)
            if Device_Type:
                alert_list = alert_list.filter(Type=Device_Type)

            if hostname:
                alert_list = alert_list.filter(Typename=hostname)
            if ip:
                alert_list = alert_list.filter(ip=ip)
            if machine:
                alert_list = alert_list.filter(message__icontains=machine)
        spm = uuid.uuid4().hex
        cache.set(spm, alert_list, 300)
        url = reverse_lazy('alarmEvents:alarmEvents_export') + '?spm=%s' % spm
        return JsonResponse({'redirect': url})

# 导出历史告警
@csrf_exempt
def alarm_his_export(request):
    if request.method == 'GET':
        # 表头预处理
        fields = [
            # field for field in Jk_Alert_His._meta.fields # 修改
            field for field in AlertHis._meta.fields # 修改
            if field.name not in [
                'eventid', 'zabbix_id', 'Status', 'Deal_Details', 'Deal_End_time', 'Alert_His_id'
            ]
        ]
        # 表名
        filename = '{}-alarm_His.xls'.format(
            time.strftime("%Y-%m-%d", time.localtime(time.time()))
        )

        def _map_header(field_name):
            header_dic = {
            'Alert_His_id':  '告警信息ID',
            'Alert_lev_id':  '告警级别',
            'Application':  '所属应用',
            'Type':  '所属设备',
            'Typename':  '设备名',
            'ip':  '设备IP',
            'item': '监控项',
            'message':  '告警内容',
            'Oc_time':  '发生时间',
            'End_time':  '结束时间',
            'A_time':  '受理时间',
            'Sendto':  '通告人',
            'Status':  '受理结果 ',
            'Deal_Person':  '处理人',
            'Deal_Details':  '受理内容',
            'Deal_End_time':  '处理完成时间',
            'DESC':  '描述'
            }
            return header_dic[field_name]

        header = [_map_header(str(field.name)) for field in fields]
        spm = request.GET.get('spm', '')  # <QueryDict: {'spm': ['6d48f7c0559242569fc6df8198fbfa26']}>
        if spm:
            alert_list = cache.get(spm)
        # 写入excel
        wb = xlwt.Workbook(encoding='utf-8')
        sheet_1 = wb.add_sheet(u'历史告警')
        for i in range(len(header)):
            sheet_1.write(0, i, header[i])
        ip_list = get_ip_list(request.user)
        for index, alert in enumerate(alert_list):
            # if isinstance(alert, Jk_Alert_His):      #修改
            if isinstance(alert, AlertHis):
                AppName = ip_list[alert.ip]
                data = [getattr(alert, field.name) for field in fields]
                for i in range(len(data)):
                    if str(data[i]) == 'None':
                        sheet_1.write(index + 1, i, '')
                    elif str(fields[i].name) == 'Application':
                        sheet_1.write(index + 1, i, AppName)
                    elif str(fields[i].name) == 'Oc_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'End_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'Alert_lev_id':
                        sheet_1.write(index + 1, i, data[i].LevName)
                    elif str(fields[i].name) == 'A_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'Sendto':
                        if str(data[i]) == '':
                            sheet_1.write(index + 1, i, '')
                        else:
                            sheet_1.write(index + 1, i, 'admin')
                    else:
                        sheet_1.write(index + 1, i, str(data[i]))

            else:
                continue
        #
        # # 将生成的excel放入byte流给response
        bio = BytesIO()
        wb.save(bio)
        bio.seek(0)

        response = StreamingHttpResponse(bio)  # 直接读bio就可以，不用bio.getvalue()!!!!! 用二进制文件方式读取
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)
        return response #HttpResponse(','.join([field.name for field in fields]))

    elif request.method == 'POST':
        try:
            alerts = json.loads(request.body)
        except ValueError:
            return HttpResponse('Json object not valid', status=400)
        alert_his_ids =alerts.get('alert_his_ids', [])
        appname = request.POST.get('appname', '')
        startTime = alerts.get('startTime', '')
        endTime = alerts.get('endTime', '')
        machine =alerts.get('machine', '')
        hostname = alerts.get('hostname', '')
        ip = alerts.get('ip', '')
        Device_Type = alerts.get('Device_Type', '')
        alert_lev = alerts.get('alert_lev', 0)
        if alert_his_ids:
            # alert_list = Jk_Alert_His.objects.filter(Alert_His_id__in=alert_his_ids) # 修改
            alert_list = AlertHis.objects.filter(Alert_His_id__in=alert_his_ids)
        else:
            iplist = get_ip_list(request.user, appname)
            #alert_list = Jk_Alert_His.objects.filter(ip__in=iplist) # 修改
            alert_list = AlertHis.objects.filter(ip__in=iplist)
            if alert_lev:
                alert_list = alert_list.filter(Alert_lev_id=alert_lev)
            if Device_Type:
                alert_list = alert_list.filter(Type=Device_Type)

            if startTime and endTime:
                alert_list = alert_list.filter(
                    Q(End_time__lt=to_localtime(str(endTime)), End_time__gt=to_localtime(str(startTime))) |
                    Q(Oc_time__lt=to_localtime(str(endTime)), Oc_time__gt=to_localtime(str(startTime)))

                )
            elif not startTime and endTime:
                alert_list = alert_list.filter(
                    Q(End_time__lt=to_localtime(str(endTime))) |
                    Q(Oc_time__lt=to_localtime(str(endTime)))
                )
            elif not endTime and startTime:
                alert_list = alert_list.filter(
                    Q(End_time__gt=to_localtime(str(startTime))) |
                    Q(Oc_time__gt=to_localtime(str(startTime)))
                )
            else:
                localtime = time.time() - 60 * 60 * 24 * 7
                alert_list = alert_list.filter(
                    Q(End_time__gt=localtime) |
                    Q(Oc_time__gt=localtime)
                )
            if hostname:
                alert_list = alert_list.filter(Typename=hostname)
            if ip:
                alert_list = alert_list.filter(ip=ip)
            if machine:
                alert_list = alert_list.filter(message__icontains=machine)
        spm = uuid.uuid4().hex
        cache.set(spm, alert_list, 300)
        url = reverse_lazy('alarmEvents:alarm_his_export') + '?spm=%s' % spm
        return JsonResponse({'redirect': url})