from django.forms import ModelForm

from .models import Memoire


class MemoireForm(ModelForm):
     class Meta:
          model = Memoire
          exclude = ['created_at', 'etudiant', 'id']
          