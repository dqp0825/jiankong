# coding:utf-8
import base64
import json
import time
import uuid
import xlwt
import pickle

from io import StringIO, BytesIO
from pyzabbix import ZabbixAPI

from django.urls import reverse_lazy
from django.http import JsonResponse, StreamingHttpResponse
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse

# from dashBoard.models import JK_Shebei_Group, Jk_Mt_Information, Jk_pass, CloudDeviceToZabbix, ResourceHostToZabbix, \
#     StorageToZabbix, NetworkDeviceToZabbix, ServerToZabbix, Jk_Resource_Host, Jk_Server, Jk_Cloud_Device, Jk_Storage, \
#     Jk_Switches, Jk_Routing, Jk_Fw, Jk_Fz

# 修改
from dashBoard.models import DeviceGroup, MTInformation, ZabbixPass, CloudDeviceToZabbix, ResourceHostToZabbix,\
    StorageToZabbix, NetworkDeviceToZabbix, ServerToZabbix, ResourceHost, Server, CloudDevice, Storage,\
    Switches, Routing, Fw, Fz
from users.models import User

# Create your views here.


def get_ip_list(user, appname=None):
    if user.role == 'Admin':
        username_list = [dic['username'] for dic in
                         User.objects.all().values('username')]
    elif user.role == 'Group':
        username_list = [dic['username'] for dic in
                         User.objects.filter(Q(about_relation=user) | Q(username=user.username)).values('username')]
    else:
        username_list = [str(user.username)]
    content = (Q(user__in=username_list) & Q(app_name=appname)) if appname else Q(user__in=username_list)
    serverip = ServerToZabbix.objects.filter(content)
    cloudip = CloudDeviceToZabbix.objects.filter(content)
    resourceip = ResourceHostToZabbix.objects.filter(content)
    storageip = StorageToZabbix.objects.filter(content)
    networkip = NetworkDeviceToZabbix.objects.filter(content)
    ip_list = {shebei.host_ip: shebei.app_name
                  for shebei_list in [serverip, cloudip, resourceip, storageip, networkip]
                  for shebei in shebei_list
                   }
    return ip_list


def get_zabbix_token(zabbix_id):
    if zabbix_id:
        zabbix_id = int(zabbix_id)
    # zabbix = Jk_pass.objects.get(zabbix_id=zabbix_id) # 修改
    zabbix = Pass.objects.get(zabbix_id=zabbix_id)
    url = zabbix.url
    pwd = base64.b64decode(zabbix.pwd.encode('utf-8')).decode("utf8")
    zapi = ZabbixAPI(url)
    zapi.login(zabbix.name, pwd)
    return zapi


def m_type(Oc_time, End_time):
    test_time = time.time()
    if test_time > End_time:
        return "维护结束"
    elif test_time < Oc_time:
        return "计划维护"
    else:
        return "维护期间"


# 判断是否在维护期间
def get_sign_out(ip):
    now = int(time.time())
    try:
    # information_list = Jk_Mt_Information.objects.filter(IP=ip, Oc_time__lt=now, End_time__gt=now)  # 修改
        information_list = MTInformation.objects.filter(ip=ip, oc_time__lt=now, end_time__gt=now)
    except Exception as e:
        print(e)
    if information_list:
        return '1'
    else:
        return '0'


# 将时间戳格式化
def to_strtime(data_time):
    try:
        if not isinstance(data_time, int):
            data_time = int(data_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_time))
    except TypeError as e:
        print(e)
        return data_time


# 将格式化时间转成时间戳
def to_localtime(data_time):
    return time.mktime(time.strptime(data_time, '%Y-%m-%d %H:%M:%S'))


# ------以上是通用方法------- #
@csrf_exempt
@login_required
def signbackInformation(request):
    if request.method == 'GET':

        device_group_list = DeviceGroup.objects.all()
        data_content = {
            'shebei_gurop_list': device_group_list,
        }
        return render(request, 'signbackInformation/signSackInformation.html', data_content)

    elif request.method == 'POST':
        host_ip = request.POST.get('host_ip', '')
        group = request.POST.get('group', '')
        mt_type = request.POST.get('type', '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        login_user = request.user
        ip_list = get_ip_list(login_user)
        print(ip_list)

        information_list = MTInformation.objects.filter(ip__in=ip_list)
        print(to_localtime(str(endTime)))
        print(information_list.all())
        if host_ip:
            information_list = information_list.filter(ip=host_ip)
        if group != '':
            information_list = information_list.filter(groupid__id=int(group))
        if startTime and endTime:

            information_list = information_list.filter(
                Q(oc_time__lte=to_localtime(str(endTime)), oc_time__gte=to_localtime(str(startTime))) |
                Q(oc_time__lte=to_localtime(str(startTime)), end_time__gte=to_localtime(str(startTime))) |
                Q(oc_time__lte=to_localtime(str(endTime)), end_time__gte=to_localtime(str(endTime))) |
                Q(end_time__lte=to_localtime(str(endTime)), end_time__gte=to_localtime(str(startTime)))
            )
        if mt_type == '3':
            information_list = information_list.filter(end_time__lt=time.time())
        elif mt_type == '2':
            information_list = information_list.filter(oc_time__gt=time.time())
        elif mt_type == '1':
            information_list = information_list.filter(oc_time__lte=time.time(), end_time__gte=time.time())

        if not information_list and mt_type == '0':

            if startTime and endTime:
                information_ips = information_list.filter(
                    Q(oc_time__lt=to_localtime(str(endTime)), oc_time__gt=to_localtime(str(startTime))) |
                    Q(oc_time__lt=to_localtime(str(startTime)), end_time__gt=to_localtime(str(startTime))) |
                    Q(oc_time__lt=to_localtime(str(endTime)), end_time__gt=to_localtime(str(endTime))) |
                    Q(end_time__lt=to_localtime(str(endTime)), end_time__gt=to_localtime(str(startTime)))
                ).values_list("ip")
                ip_list = list(set(ip_list).difference(set([ips[0] for ips in information_ips])))
            res = []
            # resource_host = Jk_Resource_Host.objects.filter(Ip__in=ip_list) # 修改
            resource_host = ResourceHost.objects.filter(ip__in=ip_list)

            # server = Jk_Server.objects.filter(IP__in=ip_list) # 修改
            server = Server.objects.filter(ip__in=ip_list)

            # cloud_device = Jk_Cloud_Device.objects.filter(Ip__in=ip_list) # 修改
            cloud_device = CloudDevice.objects.filter(ip__in=ip_list)

            # storage = Jk_Storage.objects.filter(Ip__in=ip_list) # 修改
            storage = Storage.objects.filter(ip__in=ip_list)

            # switches = Jk_Switches.objects.filter(Ip__in=ip_list) # 修改
            switches = Switches.objects.filter(ip__in=ip_list)

            # routing = Jk_Routing.objects.filter(Ip__in=ip_list) # 修改
            routing = Routing.objects.filter(ip__in=ip_list)

            # fw = Jk_Fw.object.filter(Ip__in=ip_list) # 修改
            fw = Fw.objects.filter(ip__in=ip_list)

            # fz = Jk_Fz.objects.filter(Ip__in=ip_list) # 修改
            fz = Fz.objects.filter(ip__in=ip_list)
            if host_ip:
                resource_host = resource_host.filter(ip=host_ip)
                server = server.filter(ip=host_ip)
                cloud_device = cloud_device.filter(ip=host_ip)
                storage = storage.filter(ip=host_ip)
                switches = switches.filter(ip=host_ip)
                routing = routing.filter(ip=host_ip)
                fw = fw.filter(ip=host_ip)
                fz = fz.filter(ip=host_ip)
            if group != '':
                resource_host = resource_host.filter(group__id=int(group))
                server = server.filter(group__id=int(group))
                cloud_device = cloud_device.filter(group__id=int(group))
                storage = storage.filter(group__id=int(group))
                switches = switches.filter(group__id=int(group))
                routing = routing.filter(group__id=int(group))
                fw = fw.filter(group__id=int(group))
                fz = fz.filter(group__id=int(group))
            if resource_host:
                for p in resource_host:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_Name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.resource_id, 'maintenanceid': '',
                        'hostid': p.hostid})
            if server:
                for p in server:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.server_id, 'maintenanceid': '',
                        'hostid': p.hostid})

            if cloud_device:
                for p in cloud_device:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.cloud_Id, 'maintenanceid': '',
                        'hostid': p.hostid})

            if storage:
                for p in storage:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_Name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.storage_Id, 'maintenanceid': '',
                        'hostid': p.hostid})

            if switches:
                for p in switches:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.Group.group_Name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.switches_id, 'maintenanceid': '',
                        'hostid': p.hostid})
            if routing:
                for p in routing:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.routing_id, 'maintenanceid': '',
                        'hostid': p.hostid})
            if fw:
                for p in fw:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.fw_id, 'maintenanceid': '',
                        'hostid': p.hostid})
            if fz:
                for p in fz:
                    res.append({"name": '', "IP": p.ip, "Oc_time": '',
                        "End_time": '', "groupname": p.group.group_name, "Zabbix_id": p.group.zabbix_id,
                        "DESC": p.desc, 'type': '正常', 'id': p.fz_id, 'maintenanceid': '',
                        'hostid': p.hostid})
            res_content = {
                "code": 0,
                "msg": "正常",
                "count": len(res),
                "data": res[(pageIndex-1)*pageSize:pageIndex*pageSize]
            }
            print(res_content, '123')
            return HttpResponse(json.dumps(res_content), content_type='application/json')

        res = []
        print(information_list, '999')
        for p in information_list[(pageIndex-1)*pageSize:pageIndex*pageSize]:
            print(p.ip)
            print(to_strtime(p.oc_time))
            try:
                res.append({"name": p.name, "IP": p.ip, "Oc_time": to_strtime(p.oc_time), "End_time": to_strtime(p.end_time),
                            "Zabbix_id":p.group.zabbix_id, "groupid": p.group.id,
                            "groupname": p.group.name, 'maintenanceid': p.maintenanceid,
                            "DESC": p.desc, 'type': m_type(p.oc_time, p.end_time), 'id': '111', 'hostid': p.hostid})
            except Exception as e:
                print(e)
        res_content = {
            "code": 0,
            "msg": "",
            "count": len(information_list),
            "data": res
        }
        print(res_content, '111')
        return HttpResponse(json.dumps(res_content), content_type='application/json')


@login_required
def host_maintenance(request):
    """设备签退(维护)"""
    if request.method == 'GET':
        res = {}
        hostids = request.GET.get('hostids', '')
        zabbix_id = request.GET.get('zabbix_id', 0)
        name = request.GET.get('name', '')
        description = request.GET.get('description', '')
        active_since = request.GET.get('active_since', '')
        active_till = request.GET.get('active_till', '')
        if not isinstance(hostids, list):
            hostids = [hostids]
        print('1'*30, hostids)
        if active_since and active_till:
            # print('1'*30, startTime, endTime)

            # information_list = Jk_Mt_Information.objects.filter(hostid__in=hostids) # 修改
            information_list = MTInformation.objects.filter(hostid__in=hostids)

            information_list = information_list.filter(
                Q(Oc_time__lte=to_localtime(active_till), Oc_time__gte=to_localtime(active_since)) |
                Q(Oc_time__lte=to_localtime(active_since), End_time__gte=to_localtime(active_since)) |
                Q(Oc_time__lte=to_localtime(active_till), End_time__gte=to_localtime(active_till)) |
                Q(End_time__lte=to_localtime(active_till), End_time__gte=to_localtime(str(active_since)))
            )
            if information_list:
                time_list = ['{}至{}'.format(to_strtime(p.Oc_time), to_strtime(p.End_time)) for p in information_list]

                create_out = {'mgs': '请避开一下时间段：{}'.format(time_list)}
                return HttpResponse(json.dumps(create_out), content_type='application/json')

        period = to_localtime(active_till) - to_localtime(active_since)
        zapi = get_zabbix_token(zabbix_id)
        timeperiod = [{"timeperiod_type": 0, "period": period}]
        try:
            create_out = zapi.maintenance.create(timeperiods=timeperiod, hostids=hostids, name=name, description=description,
                                             active_since=to_localtime(active_since), active_till=to_localtime(active_till))
        except Exception as e:
            create_out = {'mgs': str(e)}
        res.update(create_out)
        return HttpResponse(json.dumps(res), content_type='application/json')


@login_required
def host_maintenance_online(request):
    """设备上线"""
    if request.method == 'GET':
        hostids = request.GET.get('hostid', '')
        maintenanceid = request.GET.get('maintenanceid', '')
        zabbix_id = request.GET.get('zabbix_id', 0)
        zapi = get_zabbix_token(zabbix_id)
        description = request.GET.get('description', '')
        active_since = request.GET.get('active_since', '')
        active_till = request.GET.get('active_till', '')
        maintenance = zapi.maintenance.get(maintenanceids=maintenanceid)[0]

        till = int(to_localtime(active_till)) if active_till else int(time.time())
        since = int(to_localtime(active_since)) if active_since else int(maintenance["active_since"])
        description = description or maintenance["description"]
        timeperiod = [{"timeperiod_type": 0, "period": till - since}]
        # hostid = zapi.maintenance.get(maintenanceid=maintenanceid, selectHosts="extend")[0]["hosts"][0]["hostid"]
        # period = zapi.maintenance.get(maintenanceids=maintenanceid)
        # print('1'*30, period, since)
        if not isinstance(hostids, list):
            hostids = [hostids]
        try:
            res = zapi.maintenance.update(hostids=hostids, maintenanceid=maintenanceid, timeperiods=timeperiod,
                                          active_since=since, active_till=till, description=description) #, name=name, description=description)
            print('1' * 30, res)
        except Exception as e:
            res = {'mgs': str(e)}
        return HttpResponse(json.dumps(res), content_type='application/json')


@csrf_exempt
@login_required
def maintenance_export(request):
    if request.method == 'GET':
        # 表头预处理
        fields = [
            # field for field in Jk_Mt_Information._meta.fields # 修改
            field for field in MTInformation._meta.fields
            if field.name not in [
                'hostid','maintenanceid'
            ]
        ]
        print(fields, 'fields')
        # 表名
        filename = '{}-information.xls'.format(
            time.strftime("%Y-%m-%d", time.localtime(time.time()))
        )
        print(filename)
        def _map_header(field_name):
            header_dic = {
                'id': '维护信息ID',
                'ip': '设备Ip',
                'name': '维护名称',
                'oc_time': '发生时间',
                'end_time': '结束时间',
                'group': '所属设备组',
                'maintenanceid': '上线标识',
                'desc': '描述'
            }
            return header_dic[field_name]

        try:
            header = [_map_header(str(field.name)) for field in fields]
        except Exception as e:
            print(e)

        spm = request.GET.get('spm', '')  # <QueryDict: {'spm': ['6d48f7c0559242569fc6df8198fbfa26']}>
        if spm:
            information_list = pickle.loads(cache.get(spm))
            print('--' * 30, )
        # 写入excel
        wb = xlwt.Workbook(encoding='utf-8')
        sheet_1 = wb.add_sheet(u'维护信息')
        for i in range(len(header)):
            sheet_1.write(0, i, header[i])

        for index, information in enumerate(information_list):
            # if isinstance(information, Jk_Mt_Information): # 修改
            if isinstance(information, MTInformation):
                data = [getattr(information, field.name) for field in fields]
                for i in range(len(data)):
                    if str(data[i]) == 'None':
                        sheet_1.write(index + 1, i, '')
                    elif str(fields[i].name) == 'Oc_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
                    elif str(fields[i].name) == 'End_time':
                        sheet_1.write(index + 1, i, to_strtime(data[i]))
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
        print(response['Content-Disposition'])
        return response #HttpResponse(','.join([field.name for field in fields]))

    elif request.method == 'POST':
        try:
            informations = json.loads(request.body)
            print(informations, 'aaaaa')
        except ValueError:
            return HttpResponse('Json object not valid', status=400)
        maintenances_id =informations.get('maintenances_id', [])
        host_ip =informations.get('host_ip', '')
        group = informations.get('group', '')
        mt_type = informations.get('type', '')
        startTime = informations.get('startTime', '')
        endTime = informations.get('endTime', 0)
        login_user = request.user
        ip_list = get_ip_list(login_user)
        # ip_list = get_ip_list(request.usre)  # 'admin'替换成当前登录用户
        # information_list = Jk_Mt_Information.objects.filter(IP__in=ip_list) #修改
        information_list = MTInformation.objects.filter(ip__in=ip_list)
        if maintenances_id:
            information_list = information_list.filter(id=maintenances_id)
        else:
            if host_ip:
                information_list = information_list.filter(ip=host_ip)
            if group != '':
                try:
                    information_list = information_list.filter(group_id=int(group))
                except Exception as e:
                    print(e)

            if startTime and endTime:
                # print('1'*30, startTime, endTime)
                information_list = information_list.filter(
                    Q(oc_time__lte=to_localtime(str(endTime)), oc_time__gte=to_localtime(str(startTime))) |
                    Q(oc_time__lte=to_localtime(str(startTime)), end_time__gte=to_localtime(str(startTime))) |
                    Q(oc_time__lte=to_localtime(str(endTime)), end_time__gte=to_localtime(str(endTime))) |
                    Q(end_time__lte=to_localtime(str(endTime)), end_time__gte=to_localtime(str(startTime)))
                )

            if mt_type == '3':
                information_list = information_list.filter(end_time__lt=time.time())
            elif mt_type == '2':
                information_list = information_list.filter(oc_time__gt=time.time())
            elif mt_type == '1':
                information_list = information_list.filter(oc_time__lte=time.time(), end_time__gte=time.time())

        spm = uuid.uuid4().hex
        print(information_list)
        try:
            cache.set(spm, pickle.dumps(information_list), 300)
        except Exception as e:
            print(e)
        url = reverse_lazy('signbackInformation:maintenance_export') + '?spm=%s' % spm
        return JsonResponse({'redirect': url})