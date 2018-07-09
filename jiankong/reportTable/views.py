# coding:utf-8
import json
import time
import os


from django.db.models import Q
from django.http import FileResponse,JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render,HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from dashBoard.models import ServerToZabbix, CloudDeviceToZabbix, ResourceHostToZabbix
from dashBoard.models import StorageToZabbix,NetworkDeviceToZabbix,ServerToZabbix
# from dashBoard.models import Jk_Server,Jk_Fcpu,Jk_Fmem,Jk_Fdisk
# 修改 Jk_Server:物理机表 Jk_Fcpu：物理机CPU均值表
from dashBoard.models import Server

# from dashBoard.models import Jk_Resource_Host,Jk_Scpu,Jk_Smem
# 修改 Jk_Resource_Host :宿主机ID Jk_Scpu:宿主机CPU均值表 Jk_Smem:宿主机内存均值表
from dashBoard.models import ResourceHost

# from dashBoard.models import JK_Shebei_Group,Jk_User
# 修改 Jk_User：用户信息 JK_Shebei_Group：设备组表
from dashBoard.models import DeviceGroup,User

# from dashBoard.models import Jk_Cloud_Device,Jk_Ycpu,Jk_Ymem
# 修改 Jk_Cloud_Device：云主机表 Jk_Ycpu：云主机CPU均值表 Jk_Ymem：云主机内存均值表
from dashBoard.models import CloudDevice

# from dashBoard.models import Jk_Fw,Jk_Fwcpu,Jk_FwSes,Jk_Fwmem,Jk_Fwping_Pf_Ids
# 修改 Jk_Fw：防火墙 Jk_Fwcpu：防火墙CPU趋势表 Jk_FwSes：防火墙会话数均值表 Jk_Fwping_Pf_Ids：防火墙ping监控表
from dashBoard.models import Fw

# from dashBoard.models import Jk_Switches, Jk_Jcpu, Jk_Jmem, Jk_Jdl, Jk_Jping_Pf_Ids
# 修改 Jk_Switches：交换机 Jk_Jcpu：交换机CPU趋势表 Jk_Jmem：交换机内存趋势表 Jk_Jdl：交换机时延趋势表 Jk_Jping_Pf_Ids：交换机ping监控表
from dashBoard.models import Switches
# from dashBoard.models import Jk_Fz, Jk_Fzcpu, Jk_Fzmem, Jk_Fzconn, Jk_Fzping_Pf_Ids, Jk_Fzxconn,Jk_Fzconn_Pf_Ids
# 修改 Jk_Fz：标识 Jk_Fzcpu：负载均衡CPU趋势表 Jk_Fzmem：负载均衡内存趋势表
# Jk_Fzconn：负载均衡实连接均值表 Jk_Fzping_Pf_Ids：负载均衡ping监控表
# Jk_Fzxconn 负载均衡虚连接数均值表     Jk_Fzconn_Pf_Ids：负载均衡实连接监控表
from dashBoard.models import Fz
import xlsxwriter
from signbackInformation.views import  get_ip_list

# user = "Admin"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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

#获取所管理主机组
def getgroup(user):
    grouplist = []

    if user == "Admin" or user == "admin":
        # groups = JK_Shebei_Group.objects.all()  ######修改####
        groups = DeviceGroup.objects.all()
        for group in groups:
            groupdict = {}
            groupdict['id'] = group.id
            groupdict['text'] = group.Group_Name  # 缺少字段 Group_name######修改####
            grouplist.append(groupdict)
    else:
        # userid = Jk_User.objects.filter(name=user)
        # for user_id in userid:
        #     groups = JK_Shebei_Group.objects.all()
            groups = DeviceGroup.objects.all() ######修改####
            for group in groups:
                groupdict = {}
                groupdict['id'] = group.id
                groupdict['text'] = group.Group_Name  # 缺少字段 Group_name######修改####
                grouplist.append(groupdict)
    return grouplist


# 报表
def reportTable(request):
    if request.method == 'GET':
        grouplist = getgroup(request.user)

        # 物理机
        code1 = '''[[
                                        {checkbox: true, fixed: true}
                                        , {field: 'host_ip', title: '设备ip',width:'13%'}
                                        , {field: 'hostname', title: '设备名',width:'10%'}
                                        , {field: 'app_name', title: '所属应用',width:'13%'}
                                        , {field: 'max_cpu', title: 'CPU最大利用率',width:'13%'}
                                        , {field: 'min_cpu', title: 'CPU最小利用率',width:'13%'}
                                        , {field: 'avg_cpu', title: 'CPU平均利用率',width:'13%'}
                                        , {field: 'max_mem', title: '内存最大利用率',width:'13%'}
                                        , {field: 'min_mem', title: '内存最小利用率',width:'13%'}
                                        , {field: 'avg_mem', title: '内存平均利用率',width:'13%'}

                                    ]]'''
        # 宿主机
        code2 = '''
            [[
                                            {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip',width:'13%'}
                                            , {field: 'hostname', title: '设备名', width:'10%'}

                                            , {field: 'cluster', title: '所属集群',width:'13%'}
                                            , {field: 'app_name', title: '所属应用',width:'13%'}

                                            , {field: 'max_mem', title: '内存最大利用率',width:'17%'}
                                            , {field: 'min_mem', title: '内存最小利用率',width:'17%'}
                                            , {field: 'avg_mem', title: '内存平均利用率',width:'18%'}

                                        ]]
        '''
        # 云主机
        code3 = '''
                [[
                                            {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip',width:'13%'}
                                            , {field: 'hostname', title: '设备名', width:'10%'}
                                            , {field: 'data_center', title: '数据中心', width:'13%'}
                                            , {field: 'cluster', title: '所属集群', width:'13%'}
                                            , {field: 'app_name', title: '所属应用', width:'13%'}
                                            , {field: 'max_cpu', title: 'CPU最大利用率', width:'13%'}
                                            , {field: 'min_cpu', title: 'CPU最小利用率', width:'13%'}
                                            , {field: 'avg_cpu', title: 'CPU平均利用率', width:'13%'}
                                            , {field: 'max_mem', title: '内存最大利用率', width:'13%'}
                                            , {field: 'min_mem', title: '内存最小利用率', width:'13%'}
                                            , {field: 'avg_mem', title: '内存平均利用率', width:'13%'}

                                        ]]
            '''
        # 交换机
        code4 = '''
                [[
                                            {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip',width:'13%'}
                                            , {field: 'hostname', title: '设备名', width:'11%'}

                                            , {field: 'max_cpu', title: 'CPU最大利用率', width:'15%'}
                                            , {field: 'min_cpu', title: 'CPU最小利用率', width:'15%'}
                                            , {field: 'avg_cpu', title: 'CPU平均利用率', width:'15%'}
                                            , {field: 'max_mem', title: '内存最大利用率', width:'15%'}
                                            , {field: 'min_mem', title: '内存最小利用率', width:'15%'}
                                            , {field: 'avg_mem', title: '内存平均利用率', width:'15%'}
                                            , {field: 'max_sy', title: '最大时延', width:'13%'}
                                            , {field: 'min_sy', title: '最小时延', width:'13%'}
                                            , {field: 'avg_sy', title: '平均时延', width:'13%'}
                                        ]]
            '''
        # 防火墙
        code5 = '''
                [[
                                            {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip',width:'13%'}
                                            , {field: 'hostname', title: '设备名',width:'10%'}

                                            , {field: 'max_mem', title: '内存最大利用率', width:'15%'}
                                            , {field: 'min_mem', title: '内存最小利用率', width:'15%'}
                                            , {field: 'avg_mem', title: '内存平均利用率', width:'15%'}
                                            , {field: 'max_ses', title: '最大会话数', width:'15%'}
                                            , {field: 'min_ses', title: '最小会话数', width:'15%'}
                                            , {field: 'avg_ses', title: '平均会话数', width:'16%'}

                                        ]]
            '''
        # 路由器
        code6 = '''
                [[
                                             {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip',width:'13%'}
                                            , {field: 'hostname', title: '设备名', width:'10%'}

                                            , {field: 'max_cpu', title: 'CPU最大利用率', width:'15%'}
                                            , {field: 'min_cpu', title: 'CPU最小利用率', width:'15%'}
                                            , {field: 'avg_cpu', title: 'CPU平均利用率', width:'15%'}
                                            , {field: 'max_mem', title: '内存最大利用率', width:'15%'}
                                            , {field: 'min_mem', title: '内存最小利用率', width:'15%'}
                                            , {field: 'avg_mem', title: '内存平均利用率', width:'16%'}
                                            , {field: 'max_sy', title: '最大时延', width:'13%'}
                                            , {field: 'min_sy', title: '最小时延', width:'13%'}
                                            , {field: 'avg_sy', title: '平均时延', width:'13%'}
                                            , {field: 'max_packet_loss', title: '最大丢包数', width:'13%'}
                                            , {field: 'min_packet_loss', title: '最小丢包数', width:'13%'}
                                            , {field: 'avg_packet_loss', title: '平均丢包数', width:'13%'}
                                            , {field: 'max_packet_err', title: '最大错包数', width:'13%'}
                                            , {field: 'min_packet_err', title: '最小错包数', width:'13%'}
                                            , {field: 'avg_packet_err', title: '平均错包数', width:'13%'}
                                            , {field: 'max_net_usage', title: '最大带宽利用率', width:'13%'}
                                            , {field: 'min_net_usage', title: '最小带宽利用率', width:'13%'}
                                            , {field: 'avg_net_usage', title: '平均带宽利用率', width:'13%'}
                                        ]]
            '''
        # 负载均衡
        code7 = '''
            [[
                                            {checkbox: true, fixed: true}
                                            , {field: 'host_ip', title: '设备ip2',width:'13%'}
                                            , {field: 'hostname', title: '设备名', width:'11%'}

                                            , {field: 'max_cpu', title: 'CPU最大利用率', width:'17%'}
                                            , {field: 'min_cpu', title: 'CPU最小利用率', width:'17%'}
                                            , {field: 'avg_cpu', title: 'CPU平均利用率', width:'17%'}

                                            , {field: 'fzconn', title: '实连接数', width:'13%'}
                                            , {field: 'max_xconn', title: '最大虚连接数', width:'13%'}
                                            , {field: 'min_xconn', title: '最小虚连接数', width:'13%'}
                                            , {field: 'avg_xconn', title: '平均虚连接数', width:'13%'}

                                            ]]
            '''

        url1 = "/reportTable/serverrpt/"                                #物理机
        url2 = "/reportTable/resourcehostrpt/"                          #宿主机
        url3 = "/reportTable/cloudrpt/"                                 #云主机
        url4 = "/reportTable/switchrpt/"                                #交换机
        url7 = "/reportTable/fzrpt/"                                    #负载均衡
        url8 = "/reportTable/fwrpt/"                                     #防火墙

        data = {"grouplist": grouplist, "url1": url1, "url2": url2, "url3": url3, "url4": url4,
                "url7": url7, "url8": url8,
                "code1": code1, "code2": code2, "code3": code3, "code4": code4, "code5": code5,
                "code6": code6, "code7": code7}

        return render(request,'reportTable/report.html',data)
    elif request.method == 'POST':
        groups = request.POST.get("groups", '')
        hostip = request.POST.get('hostip', '')
        ips = []
        if groups:
            for group in groups:
                pass
        pass



#时间转换
def gettime(times):
    # 转换成时间数组
    timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp


#物理机报表
@csrf_exempt
def ServerRpt(request):
    if request.method == "POST":
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        #判断结束时间
        if endTime:
            #日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            #如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        #判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',  time.localtime(endTime-7*24*3600)),'%Y-%m-%d %H:%M:%S')))

        rpt = []
        if host:
            hosts = ServerToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts)== 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0,"data":[]}))
        else:
            hosts = ServerToZabbix.objects.filter(user=request.user)

        count = 0
        totalcount=len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            mindisk = []
            maxdisk = []
            avgdisk = []
            rptdict = {}
            rptdict['host_ip'] = (i.host_ip).replace('\t','')
            rptdict['hostname'] = (i.hostname).replace('\t','')
            rptdict['app_name'] = i.app_name

            #获取主机信息
            # host = Jk_Server.objects.filter(IP=(i.host_ip).replace('\t','')).first() ####修改
            host = Server.objects.filter(IP=(i.host_ip).replace('\t','')).first()

            #获取CPU信息
            for cpu in Jk_Fcpu.objects.filter(Server_Id_id=host.Server_id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime): # 缺少字段
                maxcpu.append(cpu.Max_Cpu)
                mincpu.append(cpu.Min_Cpu)
                avgcpu.append(float(cpu.AVG_Cpu))

            # print(maxcpu,mincpu,avgcpu)

            if maxcpu and maxcpu and avgcpu:
                rptdict['min_cpu'] = str(min(mincpu))+"%"
                rptdict['max_cpu'] = str(max(maxcpu))+"%"
                rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu)/len(avgcpu))))+"%"


            #获取内存信息
            for mem in Jk_Fmem.objects.filter(Server_Id_id=host.Server_id)\
                    .filter(Name="物理内存利用率").filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxmem.append(mem.Max_Mem)
                minmem.append(mem.Min_Mem)
                avgmem.append(float(mem.AVG_Mem))
            if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                rptdict['min_mem'] = str(min(minmem))+"%"
                rptdict['max_mem'] = str(max(maxmem))+"%"
                rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem)/len(avgmem))))+"%"

            #
            # 获取磁盘信息
            for disk in Jk_Fdisk.objects.filter(Server_Id_id=host.Server_id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxdisk.append(disk.Max_Disk)
                mindisk.append(disk.Min_Disk)
                avgdisk.append(float(disk.AVG_Disk))

            if len(mindisk)>0 and len(maxdisk)>0 and len(avgcpu)>0:
                rptdict['min_disk'] = min(mindisk)
                rptdict['now_disk'] = max(maxdisk)
                rptdict['avg_disk'] = float('%.4f' % (sum(avgdisk) / len(avgdisk)))

            rpt.append(rptdict)
            count += 1
        # print(rpt)
        datajson = {"code": 0, "msg": "", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data":[]}))



#生成json数据，方便导出报表
def datavalue(keys, datas):
    datalist = []
    #数据拼接成json
    for data in datas:
        datadict = {}
        for i,v in keys.items():
            datadict[i] = data[v]
        datalist.append(datadict)
    # 创建文件
    workbook = xlsxwriter.Workbook(os.path.join(BASE_DIR, 'exportfile/file.xls'))
    # 创建工作薄
    worksheet = workbook.add_worksheet()
    # alldatalist = []
    i = 0
    for ip in keys:
        # print("11111111")
        # print(ip)
        worksheet.write(0, i, ip)
        i = i + 1

        # 写入其他行：
    i = 1
    for values in datalist:
        # 写入该行内容：
        # print(values)
        j = 0
        for index, value in values.items():
            worksheet.write(i, j, value)
            j = j + 1
        i = i + 1
    workbook.close()

# from rexex import FileWrapper
def down_file(keys, datajson):

    if datajson:
        datajson = datajson
    else:
        datajson = []
    # datajson = []
    datavalue(keys, json.loads(datajson))
    file_name = os.path.join(BASE_DIR, 'exportfile/file.xls')
    wrapper = open(file_name, 'rb')
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="file.xls"'

    return response





#报表导出
def ExportFile(request):
    if request.method == "POST":

        datajson = request.POST.get("datajson", '')
        #判断报表类型
        types = request.POST.get("type", '')
        # print(datajson)
        # print(types)
        if types == "0":
            print(datajson)
            #云主机
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "数据中心":"data_center","集群":"cluster",
                    "所属应用": "app_name", "CPU最大利用率": "max_cpu",
                    "CPU最小利用率": "min_cpu", "CPU平均利用率": "avg_cpu", "内存最小利用率": "min_mem",
                    "内存最大利用率": "max_mem", "内存平均利用率": "avg_mem"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status": "0", "code": "0"})
            except:
                return JsonResponse({"status": "1", "code": "1"})
        elif types == "1":
            #宿主机
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "数据中心": "data_center", "集群": "cluster", "所属应用": "app_name",
                     "内存最小利用率": "min_mem",
                    "内存最大利用率": "max_mem", "内存平均利用率": "avg_mem"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status": "0", "code": "0"})
            except:
                return JsonResponse({"status": "1", "code": "1"})
            pass
        elif types == "2" or types == "3":
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "所属应用": "app_name", "CPU最大利用率": "max_cpu",
                    "CPU最小利用率": "min_cpu", "CPU平均利用率": "avg_cpu", "内存最小利用率": "min_mem",
                    "内存最大利用率": "max_mem", "内存平均利用率": "avg_mem"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status":"0","code":"0"})
            except:
                return JsonResponse({"status":"1","code":"1"})



        elif types == "4":
           #交换机
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "所属应用": "app_name", "CPU最大利用率": "max_cpu",
                    "CPU最小利用率": "min_cpu", "CPU平均利用率": "avg_cpu", "内存最小利用率": "min_mem",
                    "内存最大利用率": "max_mem", "内存平均利用率": "avg_mem","最大时延":"max_sy","最小时延":"min_sy",
                    "平均时延":"avg_sy"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status":"0","code":"0"})
            except:
                return JsonResponse({"status":"1","code":"1"})

        elif types == "5":
            #负载均衡
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "所属应用": "app_name", "CPU最大利用率": "max_cpu",
                    "CPU最小利用率": "min_cpu", "CPU平均利用率": "avg_cpu", "实连接":"fzconn", "最大虚连接": "max_xconn", "最小虚连接": "min_xconn",
                    "平均虚连接": "avg_xconn"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status": "0", "code": "0"})
            except:
                return JsonResponse({"status": "1", "code": "1"})

        elif types == "6":
            # print(datajson)
            # 防火墙
            keys = {"设备IP": "host_ip", "设备名称": "hostname", "所属应用": "app_name", "内存最小利用率": "min_mem",
                    "内存最大利用率": "max_mem", "内存平均利用率": "avg_mem", "最大会话数": "max_ses",
                    "最小会话数":"min_ses","平均会话数":"avg_ses"}
            try:
                rsp = down_file(keys, datajson)
                return JsonResponse({"status": "0", "code": "0"})
            except:
                return JsonResponse({"status": "1", "code": "1"})
            pass
        elif types == "7":
            pass
    return HttpResponse([])


def getfiletest(request):
    file = open(os.path.join(BASE_DIR, 'exportfile/file.xls'), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="file.xls"'
    return response


#宿主机报表
@csrf_exempt
def ResourceHostRpt(request):
    '''
          , {field: 'max_cpu', title: 'CPU最大利用率'}
          , {field: 'min_cpu', title: 'CPU最小利用率'}
          , {field: 'avg_cpu', title: 'CPU平均利用率'}
    cpu使用率 内存有问题
    :param request:
    :return:
    '''
    if request.method == "POST":
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        #判断结束时间
        if endTime:
            #日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            #如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        #判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',  time.localtime(endTime-7*24*3600)),'%Y-%m-%d %H:%M:%S')))


        rpt = []
        # hosts = ResourceHostToZabbix.objects.filter(user=user)
        if host:
            hosts = ResourceHostToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts) == 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))
        else:
            hosts = ResourceHostToZabbix.objects.filter(user=request.user)

        # print(hosts)
        count = 0
        totalcount = len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            mindisk = []
            maxdisk = []
            avgdisk = []
            rptdict = {}
            rptdict['host_ip'] = (i.host_ip).replace('\t','')
            rptdict['hostname'] = (i.hostname).replace('\t','')
            rptdict['app_name'] = i.app_name
            # print(i.host_ip)
            #获取主机信息
            host = Jk_Resource_Host.objects.filter(Ip=(i.host_ip).replace('\t','')).first()
            # print(host)
            #获取CPU信息
            for cpu in Jk_Scpu.objects.filter(Resource_Id_id=host.Resource_Id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxcpu.append(cpu.Max_Cpu)
                mincpu.append(cpu.Min_Cpu)
                avgcpu.append(float(cpu.AVG_Cpu))

            if maxcpu and maxcpu and avgcpu:
                rptdict['min_cpu'] = str(min(mincpu))+"%"
                rptdict['max_cpu'] = str(max(maxcpu))+"%"
                rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu)/len(avgcpu))))+"%"


            #获取内存信息
            for mem in Jk_Smem.objects.filter(Resource_Id_id=host.Resource_Id)\
                    .filter(Name="Used Memory %").filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxmem.append(mem.Max_Mem)
                minmem.append(mem.Min_Mem)
                avgmem.append(float(mem.AVG_Mem))
            if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                rptdict['min_mem'] = str(min(minmem))+"%"
                rptdict['max_mem'] = str(max(maxmem))+"%"
                rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem)/len(avgmem))))+"%"

            rptdict['cluster'] = i.cluster
            rptdict['data_center'] = i.data_center
            rpt.append(rptdict)
            count += 1
        datajson = {"code": 0, "msg": "", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))


#云主机报表
@csrf_exempt
def CloudRpt(request):
    '''
    内存使用率有问题，待修正
    :param request:
    :return:
    '''
    if request.method == "POST":
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        #判断结束时间
        if endTime:
            #日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            #如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        #判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',
                            time.localtime(endTime-7*24*3600)),'%Y-%m-%d %H:%M:%S')))


        rpt = []
        if host:
            hosts = CloudDeviceToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts) == 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))
        else:
            hosts = CloudDeviceToZabbix.objects.filter(user=request.user)

        count = 0
        totalcount = len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            mindisk = []
            maxdisk = []
            avgdisk = []
            rptdict = {}
            rptdict['host_ip'] = i.host_ip
            rptdict['hostname'] = i.hostname
            rptdict['app_name'] = i.app_name

            # print(i.host_ip)
            #获取主机信息
            host = Jk_Cloud_Device.objects.filter(Ip=i.host_ip).first()
            print("2222")
            print(host.Ip, host.CloudDeviceName)
            #获取CPU信息
            for cpu in Jk_Ycpu.objects.filter(Cloud_Id_id=host.Cloud_Id)\
                    .filter(Name="CPU利用率").filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxcpu.append(cpu.Max_Cpu)
                mincpu.append(cpu.Min_Cpu)
                avgcpu.append(float(cpu.AVG_Cpu))

            if maxcpu and maxcpu and avgcpu:
                rptdict['min_cpu'] = str(min(mincpu))+"%"
                rptdict['max_cpu'] = str(max(maxcpu))+"%"
                rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu)/len(avgcpu))))+"%"


            #获取内存信息
            for mem in Jk_Ymem.objects.filter(Cloud_Id_id=host.Cloud_Id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxmem.append(mem.Max_Mem)
                minmem.append(mem.Min_Mem)
                avgmem.append(float(mem.AVG_Mem))
            if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                rptdict['min_mem'] = str(min(minmem))+"%"
                rptdict['max_mem'] = str(max(maxmem))+"%"
                rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem)/len(avgmem))))+"%"

            rptdict['cluster'] = i.cluster
            rptdict['data_center'] = i.data_center
            rpt.append(rptdict)
            count += 1
        datajson = {"code": 0, "msg": "", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))


#防火墙报表
@csrf_exempt
def FwRpt(request):

    '''
         , {field: 'max_cpu', title: 'CPU最大利用率'}
         , {field: 'min_cpu', title: 'CPU最小利用率'}
         , {field: 'avg_cpu', title: 'CPU平均利用率'}
    ping
    :param request:
    :return:
    '''
    if request.method == "POST":
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        # 判断结束时间
        if endTime:
            # 日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            # 如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        # 判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(
                time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(endTime - 7 * 24 * 3600)),
                              '%Y-%m-%d %H:%M:%S')))

        rpt = []
        # hosts = ResourceHostToZabbix.objects.filter(user=user)
        if host:

            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts) == 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))
        else:
            print("11111")
            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user)

        # print(hosts)
        count = 0
        totalcount = len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            minses = []
            maxses= []
            avgses = []
            rptdict = {}
            rptdict['host_ip'] = i.host_ip
            rptdict['hostname'] = i.hostname
            # rptdict['app_name'] = i.Application
            # print(i.host_ip)
            # 获取主机信息

            # host = Jk_Fw.objects.filter(Ip=i.host_ip).first()
            host = Fw.objects.filter(Ip=i.host_ip).first() # 修改 ###########
            print(host)
            if host:
                # 获取CPU信息
                for cpu in Jk_Fwcpu.objects.filter(Fw_id_id=host.Fw_id) \
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    maxcpu.append(cpu.Max_Cpu)
                    mincpu.append(cpu.Min_Cpu)
                    avgcpu.append(float(cpu.AVG_Cpu))

                if maxcpu and maxcpu and avgcpu:
                    rptdict['min_cpu'] = str(min(mincpu))+"%"
                    rptdict['max_cpu'] = str(max(maxcpu))+"%"
                    rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu) / len(avgcpu))))+"%"

                # 获取内存信息
                for mem in Jk_Fwmem.objects.filter(Fw_id_id=host.Fw_id) \
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    maxmem.append(mem.Max_Mem)
                    minmem.append(mem.Min_Mem)
                    avgmem.append(float(mem.AVG_Mem))
                if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                    rptdict['min_mem'] = str(min(minmem))+"%"
                    rptdict['max_mem'] = str(max(maxmem))+"%"
                    rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem) / len(avgmem))))+"%"
                else:
                    rptdict['min_mem'] = ""
                    rptdict['max_mem'] = ""
                    rptdict['avg_mem'] = ""

                # 获取ping,取所选时间段最后一次的ping值
                ping = Jk_Fwping_Pf_Ids.objects.filter(Fw_id_id=host.Fw_id).filter(Clock__gte=startTime).filter(
                    Clock__lte=endTime).last()
                rptdict['ping'] = ping.Value

                #会话数
                for ses in Jk_FwSes.objects.filter(Fw_id_id=host.Fw_id) \
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    maxses.append(ses.Max_Hh)
                    minses.append(ses.Min_Hh)
                    avgses.append(float(ses.AVG_Hh))

                if len(minses) > 0 and len(maxses) > 0 and len(avgses) > 0:
                    rptdict['min_ses'] = min(minses)
                    rptdict['max_ses'] = max(maxses)
                    rptdict['avg_ses'] = float('%.4f' % (sum(avgses) / len(avgses)))




                rptdict['cluster'] = "Ucloud-Paas"
                rptdict['data_center'] = "亦庄数据中心"
                rpt.append(rptdict)
                count += 1
        datajson = {"code": 0, "msg": "123", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))


#交换机报表
@csrf_exempt
def SwitchRpt(request):
    '''
     , {field: 'max_packet_loss', title: '最大丢包数', width:120}
                                            , {field: 'min_packet_loss', title: '最小丢包数', width:120}
                                            , {field: 'avg_packet_loss', title: '平均丢包数', width:120}
                                            , {field: 'max_packet_err', title: '最大错包数', width:120}
                                            , {field: 'min_packet_err', title: '最小错包数', width:120}
                                            , {field: 'avg_packet_err', title: '平均错包数', width:120}
                                            , {field: 'max_net_usage', title: '最大带宽利用率', width:120}
                                            , {field: 'min_net_usage', title: '最小带宽利用率', width:120}
                                            , {field: 'avg_net_usage', title: '平均带宽利用率', width:120}
    :param request:
    :return:
    '''
    if request.method == "GET":
        # print(request.POST.get('page', '111'))
        pageIndex = int(request.POST.get('page', '1'))
        pageSize = int(request.POST.get('limit', '10'))

        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        #判断结束时间
        if endTime:
            #日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            #如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        #判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',  time.localtime(endTime-7*24*3600)),'%Y-%m-%d %H:%M:%S')))


        rpt = []
        # hosts = ResourceHostToZabbix.objects.filter(user=user)
        if host:
            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts) == 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))
        else:
            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user)

        # print(hosts)
        count = 0
        totalcount = len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            minsy = []
            maxsy = []
            avgsy = []
            rptdict = {}
            rptdict['host_ip'] = (i.host_ip).replace('\t','')
            rptdict['hostname'] = (i.hostname).replace('\t','')
            # rptdict['app_name'] = i.Application
            # print(i.host_ip)
            #获取主机信息
            # host = Jk_Switches.objects.filter(Ip=(i.host_ip).replace('\t','')).first() # 修改
            host = Switches.objects.filter(Ip=(i.host_ip).replace('\t','')).first()
            # print(host)

            #获取CPU信息
            for cpu in Jk_Jcpu.objects.filter(Switches_Id_id=host.Switches_Id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime): # 缺少字段
                maxcpu.append(cpu.Max_Cpu)
                mincpu.append(cpu.Min_Cpu)
                avgcpu.append(float(cpu.AVG_Cpu))

            if maxcpu and maxcpu and avgcpu:
                rptdict['min_cpu'] = str(min(mincpu))+"%"
                rptdict['max_cpu'] = str(max(maxcpu))+"%"
                rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu)/len(avgcpu))))+"%"


            #获取内存信息
            for mem in Jk_Jmem.objects.filter(Switches_Id_id=host.Switches_Id)\
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxmem.append(mem.Max_Mem)
                minmem.append(mem.Min_Mem)
                avgmem.append(float(mem.AVG_Mem))
            if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                rptdict['min_mem'] = str(min(minmem))+"%"
                rptdict['max_mem'] = str(max(maxmem))+"%"
                rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem)/len(avgmem))))+"%"

            #获取时延信息
            for sy in Jk_Jdl.objects.filter(Switches_Id_id=host.Switches_Id) \
                    .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                maxsy.append(sy.Max_Sy)
                minsy.append(sy.Min_Sy)
                avgsy.append(float(sy.AVG_Sy))
            if len(minsy) > 0 and len(maxsy) > 0 and len(avgsy) > 0:
                rptdict['min_sy'] = min(minsy)
                rptdict['max_sy'] = max(maxsy)
                rptdict['avg_sy'] = float('%.4f' % (sum(avgsy) / len(avgsy)))

            # 获取ping,取所选时间段最后一次的ping值
            ping =  Jk_Jping_Pf_Ids.objects.filter(Switches_Id_id=host.Switches_Id).filter(Clock__gte=startTime).filter(Clock__lte=endTime).last()

            rptdict['ping'] = ping.Value
            rptdict['cluster'] = "Ucloud-Paas"
            rptdict['data_center'] = "亦庄数据中心"
            rpt.append(rptdict)
            count += 1
        datajson = {"code": 0, "msg": "123", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))


#负载均衡报表
@csrf_exempt
def FzRpt(request):
    '''
        , {field: 'max_mem', title: '内存最大利用率', width:120}
        , {field: 'min_mem', title: '内存最小利用率', width:120}
        , {field: 'avg_mem', title: '内存平均利用率', width:120}
         "内存最小利用率": "min_mem",
         "内存最大利用率": "max_mem",
         "内存平均利用率": "avg_mem",

    :param request:
    :return:
    '''
    if request.method == "POST":
        pageIndex = int(request.POST.get('page', ''))
        pageSize = int(request.POST.get('limit', ''))
        group = request.POST.get("group", '')
        host = request.POST.get("host", '')
        startTime = request.POST.get('startTime', '')
        endTime = request.POST.get('endTime', '')

        #判断结束时间
        if endTime:
            #日期转化为时间戳
            endTime = int(gettime(endTime))
        else:
            #如果结束时间为空，默认为当前时间
            endTime = int(time.time())

        #判断开始时间
        if startTime:

            startTime = int(gettime(startTime))

        else:
            # 如果开始时间为空，则默认开始时间为结束时间的当天00:00
            startTime = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',  time.localtime(endTime-7*24*3600)),'%Y-%m-%d %H:%M:%S')))


        rpt = []
        # hosts = ResourceHostToZabbix.objects.filter(user=user)
        # print("11111")
        if host:
            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user).filter(host_ip=host)
            if len(hosts) == 0:
                return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))
        else:
            # print(request.user)
            hosts = NetworkDeviceToZabbix.objects.filter(user=request.user)

        # print(hosts)
        count = 0
        totalcount = len(hosts)
        for i in hosts[(pageIndex - 1) * pageSize:pageIndex * pageSize]:
            mincpu = []
            maxcpu = []
            avgcpu = []
            minmem = []
            maxmem = []
            avgmem = []
            minxconn = []
            maxxconn = []
            avgxconn = []
            rptdict = {}
            rptdict['host_ip'] = i.host_ip
            rptdict['hostname'] = i.hostname
            # rptdict['app_name'] = i.Application
            print(i.host_ip)
            #获取主机信息
            # host = Jk_Fz.objects.filter(Ip=i.host_ip).first() # 修改 ####
            host = Fz.objects.filter(Ip=i.host_ip).first()

            print(host)
            if host:

                #获取CPU信息
                for cpu in Jk_Fzcpu.objects.filter(Fz_id_id=host.Fz_id)\
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    print("22222")
                    maxcpu.append(cpu.Max_Cpu)
                    mincpu.append(cpu.Min_Cpu)
                    avgcpu.append(float(cpu.AVG_Cpu))


                if maxcpu and maxcpu and avgcpu:
                    rptdict['min_cpu'] = str(min(mincpu))+"%"
                    rptdict['max_cpu'] = str(max(maxcpu))+"%"
                    rptdict['avg_cpu'] = str(float('%.4f' % (sum(avgcpu)/len(avgcpu))))+"%"


                #获取内存信息
                for mem in Jk_Fzmem.objects.filter(Fz_id_id=host.Fz_id)\
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    maxmem.append(mem.Max_Mem)
                    minmem.append(mem.Min_Mem)
                    avgmem.append(float(mem.AVG_Mem))
                if len(minmem) > 0 and len(maxmem) > 0 and len(avgmem) > 0:
                    rptdict['min_mem'] = str(min(minmem))+"%"
                    rptdict['max_mem'] = str(max(maxmem))+"%"
                    rptdict['avg_mem'] = str(float('%.4f' % (sum(avgmem)/len(avgmem))))+"%"

                #获取虚连接信息
                for xconn in Jk_Fzxconn.objects.filter(Fz_id_id=host.Fz_id) \
                        .filter(Clock__gte=startTime).filter(Clock__lte=endTime):
                    maxxconn.append(xconn.Max_Xconn)
                    minxconn.append(xconn.Min_Xconn)
                    avgxconn.append(float(xconn.AVG_Xconn))
                if len(minxconn) > 0 and len(maxxconn) > 0 and len(avgxconn) > 0:
                    rptdict['min_xconn'] = min(minxconn)
                    rptdict['max_xconn'] = max(maxxconn)
                    rptdict['avg_xconn'] = float('%.4f' % (sum(avgxconn) / len(avgxconn)))

                # 获取ping,取所选时间段最后一次的ping值
                ping =  Jk_Fzping_Pf_Ids.objects.filter(Fz_id_id=host.Fz_id).filter(Clock__gte=startTime).filter(Clock__lte=endTime).last()
                rptdict['ping'] = ping.Value

                print("3333333333333")
                #获取实链接
                fzconn = Jk_Fzconn.objects.filter(Fz_id_id=host.Fz_id).filter(Clock__gte=startTime).filter(Clock__lte=endTime).last()
                rptdict['fzconn'] = fzconn.Max_Conn

                rptdict['cluster'] = "Ucloud-Paas"
                rptdict['data_center'] = "亦庄数据中心"
                rpt.append(rptdict)
                count += 1

        datajson = {"code": 0, "msg": "123", "count": totalcount, "data": rpt}
        return HttpResponse(json.dumps(datajson))
    return HttpResponse(json.dumps({"code": 0, "msg": "", "count": 0, "data": []}))