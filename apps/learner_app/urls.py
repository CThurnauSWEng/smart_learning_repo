from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^learner_dashboard', views.learner_dashboard),    
    url(r'^quiz/(?P<subject_id>\d+)$', views.start_quiz),    
    url(r'^remove/(?P<subject_id>\d+)$', views.remove),    
    url(r'^add_subject/(?P<subject_id>\d+)$', views.add_subject),    
    url(r'^learner_home', views.learner_home)     
]

