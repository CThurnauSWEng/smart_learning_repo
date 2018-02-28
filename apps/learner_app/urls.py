from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^learner_dashboard', views.learner_dashboard),    
    url(r'^quiz/(?P<subject_id>\d+)$', views.start_quiz),    
    url(r'^remove/(?P<subject_id>\d+)$', views.remove),    
    url(r'^add_subject/(?P<subject_id>\d+)$', views.add_subject),    
    url(r'^check_answer', views.check_answer),     
    url(r'^show_answer', views.show_answer),     
    url(r'^display_next_card', views.display_next_card),     
    url(r'^learner_home', views.learner_home)     
]

