from django.urls import path

from . import views
app_name = "application_web_aky"

urlpatterns = [
   
    path('', views.index, name='index'),
   
    path('admin', views.home_admin, name='home_admin'),
   
    path('etudiant', views.home_etudiant, name='home_etudiant'),
   
    path('etudiant/deposer/', views.deposer, name='deposer'),
   
    path('rechercher/', views.rechercher, name="rechercher"),

    path('admin/autoriser/', views.autoriser, name='autoriser'),  
   
    path('etudiant/profile', views.profile, name='profile'),
   
    path('admin/profile', views.profile, name='profile'),

    path('consulter', views.consulter, name='consulter'),
    ]
