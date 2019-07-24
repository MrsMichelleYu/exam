from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^groups$', views.groups),
    url(r'^create$', views.create),
    url(r'^groups/(?P<id>\d+)$', views.details),
    url(r'^leave/(?P<id>\d+)$', views.leave),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
