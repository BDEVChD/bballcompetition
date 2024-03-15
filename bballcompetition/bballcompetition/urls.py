"""
URL configuration for bballcompetition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from bballcompapp.views import home
from bballcompapp.views import trackerpage
from bballcompapp.views import notificationhome


urlpatterns = [
    path('admin/', admin.site.urls),
    path('trackerpage/', trackerpage, name='trackerpage'),
    path('', notificationhome, name='notificationhome'), 
]
