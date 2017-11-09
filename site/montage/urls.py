"""montage URL Configuration

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

from recsys import views as rec_views
from abloop import views as abloop_views
from redlev import views as redlev_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rec-sys/', include('recsys.urls')),
    url(r'^ab-loop/', abloop_views.index),
    url(r'^red-lev/', redlev_views.index),
    url(r'^$', rec_views.index),
]
