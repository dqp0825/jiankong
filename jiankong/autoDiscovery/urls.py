from django.conf.urls import url
from .  import views
urlpatterns = [
    url(r'autoDiscovery',views.autoDiscovery,name='autoDiscovery'),
    url(r'getautodiscovery',views.getautodiscovery,name='getautodiscovery'),
]
