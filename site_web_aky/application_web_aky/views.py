from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.http.response import FileResponse, HttpResponse
from django.conf import settings
from django.contrib import messages

from itertools import chain
import requests
import os
import json

from .forms import MemoireForm
from .models import (
     Etablissement,
     Etudiant,
     Administrateur,
     Parcours,
     Memoire,
     Theme
)


def index(request):
     if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          
          user = auth.authenticate(
               username=username,
               password=password
          )
          if user is not None:
               auth.login(request, user)
               # determiner le type de l'utilisateur
               adminuser = User.objects.get(username=username)
               if Etudiant.objects.filter(user=user).exists():
                    return redirect('./etudiant')
               return redirect('./admin')
          return redirect('./')
     return render(request, 'index.html')


def home_admin(request):
     return render(request, 'admin_home.html')

def autoriser(request):
     if request.user.is_authenticated:
          user = User.objects.get(username=request.user.username)
          if Administrateur.objects.filter(user=user).exists():
               if request.method == 'POST':
                    form_ids = request.POST.getlist('user_id')
                    ids_deposer = Etudiant.objects.all().filter(deposer=True).values('user_id')
                    # L'admin veut ôter le droit de déposer à un étudiant ayant le droit et qui n'a pas encore déposer son mémoire
                    for id_deposer in ids_deposer:
                         if id_deposer not in form_ids:
                              Etudiant.objects.filter(user_id=id_deposer['user_id']).update(deposer=False)
                    # L'admin attribue le droit de déposer à un étudiant
                    for user_id in form_ids:
                         etudiant = Etudiant.objects.filter(user_id=user_id).get()
                         etudiant.deposer = True
                         etudiant.save()
                    return render(request, 'autorisation_reussie.html')
               admin = Administrateur.objects.get(user=user)
               parcours = Parcours.objects.filter(adminstrateur=admin)
               etudiants = []
               for parc in parcours:
                    etudiant_parcours  = Etudiant.objects.filter(parcours=parc)
                    for etu in etudiant_parcours:
                         etudiant_dict = {}
                         user = User.objects.get(etudiant=etu)
                         memoire = Memoire.objects.filter(etudiant=etu)
                         if not memoire.exists():
                              etudiant_dict['user_id'] = user.id
                              etudiant_dict['no_carte'] = etu.no_carte
                              etudiant_dict['deposer'] = etu.deposer
                              etudiant_dict['nom'] = user.last_name
                              etudiant_dict['prenoms'] = user.first_name
                              etudiants.append(etudiant_dict)
               context = {
                    'etudiants': etudiants
               }
               return render(request, 'autoriser.html', context)
          return render(request, '404.html')
     return redirect('index')


def home_etudiant(request):
     return render(request, 'etudiant_home.html')



def filtrer(filtres_theme=[], filtres_parcours=[]):
     etudiants_ids, themes_ids = [], []

     if filtres_theme:
          themes = Theme.objects.filter(libelle__in=[theme.capitalize() for theme in filtres_theme]).values()
          [themes_ids.append(theme['id']) for theme in themes]
     if filtres_parcours:
          parcours = Parcours.objects.filter(
              libelle__in = [parc.title() for parc in filtres_parcours]).values('id')
          for parc in parcours:
               etudiant_filtre = Etudiant.objects.filter(parcours=parc['id']).values()
               [etudiants_ids.append(etudiant['id']) for etudiant in etudiant_filtre]
     parcours_memoires = [Memoire.objects.filter(etudiant=id).values() for id in etudiants_ids]
     theme_memoires = [Memoire.objects.filter(theme=id).values() for id in themes_ids]
     if filtres_parcours and filtres_theme:
          memoires = Memoire.objects.filter(Q(etudiant__in=etudiants_ids) & Q(theme__in=themes_ids)).values()
     elif filtres_theme:
          memoires = Memoire.objects.filter(Q(theme__in=themes_ids)).values()
     elif filtres_parcours:
          memoires = Memoire.objects.filter(Q(etudiant__in=etudiants_ids)).values()
     else:
          memoires = Memoire.objects.all().values()
     return memoires

def rechercher(request):
     if request.user.is_authenticated:
          memoires_list = []
          if request.method == 'POST':
               precedent = request.POST.getlist('precedent')
               cle = request.POST.get('mot_cle')
               filtres_annee = request.POST.getlist('annee')
               filtres_parcours = request.POST.getlist('parcours')
               filtres_theme = request.POST.getlist('theme')
               if cle:
                    if precedent:
                        memoires_precedents = Memoire.objects.filter(id__in=precedent)
                        memoires = memoires_precedents.filter(description__icontains=cle).all().values()
                    else:
                        memoires = Memoire.objects.all().values()
               else:
                    memoires = filtrer(filtres_theme=filtres_theme, filtres_parcours=filtres_parcours)
          else:
               memoires = Memoire.objects.all().values()

          for memoire in memoires:
               memoire_dict = {}
               etudiant = memoire.get('etudiant_id')
               user_etu = User.objects.filter(etudiant=etudiant).values().first()
               memoire_dict['id'] = memoire['id']
               memoire_dict['titre'] = memoire['titre']
               memoire_dict['num_ordre'] = memoire['num_ordre']
               memoire_dict['description'] = memoire['description']
               memoire_dict['auteur'] = user_etu['last_name'] + ' ' + user_etu['first_name']
               memoires_list.append(memoire_dict)
          user = User.objects.get(username=request.user.username)
          is_admin = False
          if Administrateur.objects.filter(user=user).exists():
               is_admin = True
          context = {
               'is_admin': is_admin,
               'memoires': memoires_list,
               'resultats': len(memoires_list)
          }
          return render(request, 'recherche.html', context)
     return redirect("index")

def deposer(request):
     user = User.objects.get(username=request.user.username)
     etudiant = Etudiant.objects.get(user=user)
     if etudiant.deposer:
          if request.method == 'POST':
               form_depot = MemoireForm(request.POST, request.FILES)
               if form_depot.is_valid():
                    num_ordre = form_depot.cleaned_data['num_ordre']
                    titre = form_depot.cleaned_data['titre']
                    description = form_depot.cleaned_data['description']
                    media = form_depot.cleaned_data['media']
                    theme = form_depot.cleaned_data['theme']
                    memoire = Memoire(
                         etudiant=etudiant,
                         num_ordre=num_ordre,
                         titre=titre,
                         description=description,
                         media=media,
                         theme=theme
                    )
                    etudiant.deposer = False
                    memoire.save()
                    etudiant.save()
                    return redirect('index')
               messages.info(request, 'Votre formualire n\'est pas valide !!!')
               return redirect('index')
     else:
          messages.info(request, 'Vous n\'êtes pas autorisé à faire un dépôt !!!')
     form_depot = MemoireForm()
     context = {
          'form': form_depot,
          'etudiant': etudiant
     }

     return render(request, 'depot.html', context)


def consulter(request, memoire_pk):
     memoire = Memoire.objects.filter(id=memoire_pk)
     if memoire.exists():
          try:
               file_name = str(memoire.get().media)
               file_path = os.path.join(settings.MEDIA_ROOT, file_name)
               return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
          except FileNotFoundError:
               print('Not found file')
     return redirect('./')


def profile(request):
     if request.user.is_authenticated:
          is_admin = True
          etablissement = ""
          user = User.objects.get(username=request.user.username)
          if Etudiant.objects.filter(user=user).exists() and request.get_full_path() == '/aky/etudiant/profile':
               is_admin = False
               profile = Etudiant.objects.get(user=user)
               parcours = profile.parcours
               etablissement = parcours.etablissement
          elif Administrateur.objects.filter(user=user) and request.get_full_path() == '/aky/admin/profile':
               profile = Administrateur.objects.filter(user=user).get()
               parcours = Parcours.objects.filter(adminstrateur=profile)
               etablissement = parcours[0].etablissement
               libelles = []
               for parc in parcours:
                    libelles.append(parc.libelle)
               parcours = []
               for i, libelle in enumerate(libelles):
                    parcours.append({'num': i + 1, 'libelle': libelle})
          else:
               return render(request, '404.html')
          context = {
               'user': user,
               'profile': profile,
               'is_admin': is_admin,
               'parcours': parcours,
               'etablissement': etablissement
          }
          return render(request, 'profile.html', context)
     return redirect('index')




