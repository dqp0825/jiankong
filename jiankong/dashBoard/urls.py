from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'dashBoard',views.dashBoard,name='dashBoard'),
    url(r'dealalarm',views.dealalarm,name='dealalarm'),
    url(r'maintaininfo',views.maintaininfo,name='maintaininfo'),
]
