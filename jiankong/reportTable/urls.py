from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'reportTable',views.reportTable,name='reportTable'),
    url(r'serverrpt',views.ServerRpt,name='serverrpt'),
    url(r'resourcehostrpt',views.ResourceHostRpt,name='resourcehostrpt'),
    url(r'cloudrpt',views.CloudRpt,name='cloudrpt'),
    url(r'fwrpt',views.FwRpt,name='fwrpt'),
    url(r'switchrpt',views.SwitchRpt,name='switchrpt'),
    url(r'fzrpt',views.FzRpt,name='fzrpt'),
    url(r'exportfile', views.ExportFile, name='exportfile'),
    url(r'getfiletest', views.getfiletest, name='getfiletest'),
    # url(r'getgroup',views.getgroup,name='getgroup'),
]
