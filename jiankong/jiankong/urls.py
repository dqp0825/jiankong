"""jiankong URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dashBoard import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^alarmEvents/', include(('alarmEvents.urls','alarmEvents'), namespace='alarmEvents')),
    url(r'^dashBoard/', include(('dashBoard.urls','alarmEvents'),namespace='dashBoard')),
    url(r'^realtimeMonitor/', include(('realtimeMonitor.urls','realtimeMonitor'), namespace='realtimeMonitor')),
    url(r'^signbackInformation/', include(('signbackInformation.urls','signbackInformation') ,namespace='signbackInformation')),
    url(r'^autoDiscovery/', include(('autoDiscovery.urls','autoDiscovery') ,namespace='autoDiscovery')),
    url(r'^monitorItems/', include(('monitorItems.urls','monitorItems'), namespace='monitorItems')),
    url(r'^reportTable/', include(('reportTable.urls','reportTable'), namespace='reportTable')),
    url(r'^topologyView/', include(('topologyView.urls','topologyView'), namespace='topologyView')),
    url(r'^index/', views.index, name='index'),
    url(r'^users/', include(('users.urls.views_urls','users'), namespace='users')),

]
