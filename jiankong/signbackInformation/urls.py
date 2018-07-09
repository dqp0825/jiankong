from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'signbackInformation/', views.signbackInformation, name='signbackInformation'),
    url(r'host_maintenance/', views.host_maintenance, name='host_maintenance'),  # 签退
    url(r'host_maintenance_online/', views.host_maintenance_online, name='host_maintenance_online'),  # 上线
    url(r'maintenance_export/', views.maintenance_export, name='maintenance_export'),  # 导出
]
