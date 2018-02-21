from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),    
    url(r'^logout', views.logout),     
    url(r'^process_login', views.process_login),     
    url(r'^process_register', views.process_register),     
]

