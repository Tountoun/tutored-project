from django.urls import path

from . import views
app_name = "application_web_aky"

urlpatterns = [
   
    path('', views.index, name='index'),
   
    path('home/adm', views.home_admin, name='home_admin'),
   
    path('home/etu', views.home_etudiant, name='home_etudiant'),
   
    path('etudiant/deposer', views.deposer, name='etudiant_depot'),
   
    path('rechercher/', views.recherche, name="recherche"),
   
    path('etudiant/profile', views.profile, name='profile'),
   
    path('admi/profile', views.profile, name='profile'),
   
    path('depot/autoriser', views.autoriser, name='autorise'),  
    
    path('filtre/', views.filter, name='filtre'),    
  
]
