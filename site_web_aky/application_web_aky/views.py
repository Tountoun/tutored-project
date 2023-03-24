from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import requests
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