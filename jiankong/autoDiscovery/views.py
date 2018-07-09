# coding:utf-8
import json


from django.shortcuts import render,HttpResponse


# Create your views here.
# 自动发现
def autoDiscovery(request):
    if request.method == 'GET':
        return render(request,'autoDiscovery/automaticallyDiscover.html')
    elif request.method == 'POST':
        pass


#获取自动发现信息
def getautodiscovery(request):
    alertjson = {"code": 0, "msg": "", "count": 1, "data": [{"ip":"10.249.8.99","hostname":"10.249.8.99","os":"ESXI"}]}
    return HttpResponse(json.dumps(alertjson))
