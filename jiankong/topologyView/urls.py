from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'topologyView/',views.topologyView,name='topologyView'),
    # url('tuopu/', views.tuopu),
    url('bjsj/', views.bjsj),
    url('jf/', views.jf),
    url('jfxx/', views.jfxx),
    url('jftps/', views.jftps),
    url('jftp/', views.jftp),
    url('dltp/', views.dltp),
]
