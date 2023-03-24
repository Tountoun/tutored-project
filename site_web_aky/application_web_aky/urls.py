from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/home', views.admin_home, name='admin_home'),
    path('etudiant/home', views.etudiant_home, name='etudiant_home'),
]
