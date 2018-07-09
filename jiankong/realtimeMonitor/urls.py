from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'application/',views.application,name='application'),
    url(r'applicationJump/',views.applicationJump,name='applicationJump'),
    url(r'getappalert/',views.GetAppAlert,name='getappalert'),
    url(r'getappinfo/',views.getAppinfo,name='getappinfo'),
    url(r'equipmentManufacturers/',views.equipmentManufacturers,name='equipmentManufacturers'),
    url(r'equipmentManufacturersJump/',views.equipmentManufacturersJump,name='equipmentManufacturersJump'),
    url(r'physicalMachine/',views.physicalMachine,name='physicalMachine'),
    url(r'hosMachine/',views.hosMachine,name='hosMachine'),
    url(r'cloudHost/',views.cloudHost,name='cloudHost'),
    url(r'diskArray/',views.diskArray,name='diskArray'),
    url(r'fiberOpticSwitch/',views.fiberOpticSwitch,name='fiberOpticSwitch'),
    url(r'switches/',views.switches,name='switches'),
    url(r'router/',views.router,name='router'),
    url(r'loadBalancing/',views.loadBalancing,name='loadBalancing'),
    url(r'firewall/',views.firewall,name='firewall'),
    url(r'exportPhysicalMachine/',views.exportPhysicalMachine,name='exportPhysicalMachine')
]
