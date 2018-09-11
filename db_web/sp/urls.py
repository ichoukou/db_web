from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns=[
    url(r'^info/$',views.fill_info,name='fill'),
    url(r'^salary/$',views.salary_pre,name='salary'),
    url(r'^visualization/$',views.vt,name='vt'),
    url(r'^processing/$',views.processing_page,name='processing'),
    url(r'^processing1/$',views.processing1,name='processing1'),
    url(r'test/$',views.test,name='test')
]