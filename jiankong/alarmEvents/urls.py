from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'alarmEvent/',views.alarmEvent, name='alarmEvent'),
    url(r'alarm_his/', views.alarm_his, name='alarm_his'),
    url(r'host_acknowledge/', views.host_acknowledge, name='host_acknowledge'),
    url(r'alarmEvents_export/', views.alarmEvents_export, name='alarmEvents_export'),
    url(r'alarm_his_export/', views.alarm_his_export, name='alarm_his_export'),

    url(r'getalarm',views.getalarm,name='getalarm'),
    url(r'outtime',views.getalarm,name='outtime'),
]
