# coding:utf-8
import json

import requests
from django.shortcuts import render

#拓扑图
def topologyView(request):


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
    return render(request, 'tuoputu.html', {"auth": auth})

#北京数据中心
def bjsj(request):
    return render(request, 'beijingshujv.html')

#机房
def jf(request):
    return render(request, 'jf.html')

#机房详情
def jfxx(request):
    return render(request, 'jifangxinxi.html')

#机房拓扑
def jftp(request):
    return render(request, 'jifangtuopu.html')

# #大楼拓扑
def jftps(request):
    return render(request, 'jftp.html')

#大楼拓扑
def dltp(request):
    return render(request, 'daloutuopu.html')