from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^scores/', views.scores),
    url(r'^recommendations/', views.recommendations),
    url(r'^$', views.index),
]
