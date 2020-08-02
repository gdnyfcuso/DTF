"""pyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.http import HttpResponse
# from django.shortcuts import render,render_to_response

urlpatterns = [
    path("index", views.index),
    path("fundata",views.funddata),
    path('login',views.login),
    url('api/666', view=lambda e: HttpResponse('戏说不是胡说')),
    path('api/fundName',view=lambda request:HttpResponse('华夏混合')),
]
