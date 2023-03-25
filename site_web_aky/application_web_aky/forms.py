from django.forms import ModelForm, NumberInput, Select, Textarea, ModelChoiceField, FileInput

from .models import Memoire, Theme


class MemoireForm(ModelForm):
     theme = ModelChoiceField(
        queryset=Theme.objects.all(),
        widget=Select(attrs={
            'class': 'form-control',
        }),
        empty_label='Choisir le thème du mémoire'
     )
     class Meta:
          model = Memoire
          exclude = ['created_at', 'etudiant', 'id']

          widgets = {
              'num_ordre': NumberInput(attrs={
                    'class': 'form-control',
                    'style': 'max-width: 500px;',
                    'placeholder': 'Numero d\'ordre',
                    'required': True
               }),
               'titre': Textarea(attrs={
                    'class': 'form-control',
                    'style': 'rows:2; cols:10;',
                    'rows': '3',
                    'placeholder': 'Titre du mémoire',
                    'required': True
               }),
               'description': Textarea(attrs={
                    'class': 'form-control',
                    'rows': '6',
                    'placeholder': 'Description du mémoire',
                    'required': True
               }),
               'media': FileInput(attrs={
                    'class': 'form-control',
                    'style': 'max-width:500px;',
                    'placeholder': 'Fichier du mémoire',
                    'required': True,
               }),
          }
          
          