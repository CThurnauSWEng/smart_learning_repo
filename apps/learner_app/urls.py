from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^learner_dashboard', views.learner_dashboard),    
    url(r'^learner_home', views.learner_home)     
]

