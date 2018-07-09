from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'monitorItems',views.monitorItems,name='monitorItems'),
    url(r'gethostinfo',views.gethostinfo,name='gethostinfo'),
    url(r'getitem',views.getitem,name='getitem'),
]
