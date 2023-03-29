from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout, name='logout'),
    path('admin/home', views.admin_home, name='admin_home'),
    path('etudiant/home', views.etudiant_home, name='etudiant_home'),
    path('etudiant/deposer', views.deposer, name='etudiant_depot'),
    path('etudiant/profile', views.profile, name='profile'),
    path('admin/profile', views.profile, name='profile'),
    path('admin/autoriser', views.autoriser, name='autoriser'),
    re_path(r'^consulter/(?P<memoire_pk>[0-9a-f-]+)/$',
         views.consulter, name='consulter'),
]
