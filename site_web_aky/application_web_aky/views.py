from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
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
               user = User.objects.get(username=username)
               if Etudiant.objects.filter(user=user).exists():
                    return redirect('etudiant_home')
               return redirect('admin_home')
          return redirect('index')
     return render(request, 'index.html')


def admin_home(request):
     return render(request, 'admin_home.html')


def etudiant_home(request):
     return render(request, 'etudiant_home.html')


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
               messages.info(request, 'Votre formualire n\'est pas valide')
               return redirect('index')
     else:
          messages.info(request, 'Vous n\'êtes pas autorisé à faire un dépôt')
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
     return redirect('index')


def profile(request):
     user = User.objects.get(username=request.user.username)
     is_admin = True
     etablissement = ""
     if Etudiant.objects.filter(user=user).exists():
          is_admin = False
          profile = Etudiant.objects.get(user=user)
          parcours = profile.parcours
          etablissement = parcours.etablissement
     else:
          profile = Administrateur.objects.filter(user=user).get()
          parcours = Parcours.objects.filter(adminstrateur=profile)
          etablissement =parcours[0].etablissement
          libelles = []
          for parc in parcours:
               libelles.append(parc.libelle)
          parcours = []
          for i, libelle in enumerate(libelles):
               parcours.append({'num': i + 1, 'libelle': libelle})
     context = {
          'user': user,
          'profile': profile,
          'is_admin': is_admin,
          'parcours': parcours,
          'etablissement': etablissement
     }
     return render(request, 'profile.html', context)