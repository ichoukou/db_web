from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns=[
    # url(r'^test/$',views.test,name='test'),
    url(r'^index/$',views.index,name='index'),
    url(r'^search/$',views.search,name='search'),
    url(r'^search_disp/$',views.search_disp,name='search_disp'),
    url(r'^details/(?P<website>.+)/(?P<key>.+)/$',views.details,name='details'),

]