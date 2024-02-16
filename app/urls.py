# chat/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('serverStatusCheck', views.serverStatusCheck, name='serverStatusCheck'),
    path('versionPageCheck', views.versionPageCheck, name='versionPageCheck'),
    path('donationTest', views.donationTest, name='donationTest'),
    path('dev_auditionSubmit', views.dev_auditionSubmit, name='dev_auditionSubmit'),
    path('auditionVideoTest', views.auditionVideoTest, name='auditionVideoTest'),
    
    # path('appVersionCheck', views.appVersionCheck, name='appVersionCheck'),
	path('', views.index, name='index'),
    path('testttt555555', views.testttt555555, name='testttt555555'),
    path('test', views.test, name='test'),
    path('testttt333', views.testttt333, name='testttt333'),
    
    
]