from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^edit_subject/(?P<subject_id>\d+)$', views.edit_subject),    
    url(r'^edit_card/(?P<card_id>\d+)$', views.edit_card),    
    url(r'^editor_dashboard', views.editor_dashboard),    
    url(r'^create_subject', views.create_subject),    
    url(r'^process_create_subject', views.process_create_subject),    
    url(r'^create_card', views.create_card),    
    url(r'^process_create_card', views.process_create_card)     
]