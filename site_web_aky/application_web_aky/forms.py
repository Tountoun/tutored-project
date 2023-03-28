from django.forms import ModelForm, NumberInput, Select, Textarea, ModelChoiceField, FileInput

from .models import Memoire, Theme


class MemoireForm(ModelForm):
     theme = ModelChoiceField(
        queryset=Theme.objects.all(),
        widget=Select(attrs={
            'class': 'form-theme',
        }),
     )
     class Meta:
          model = Memoire
          exclude = ['created_at', 'etudiant', 'id']

          widgets = {
              'num_ordre': NumberInput(attrs={
                    'class': 'form-num',
                    'required': True
               }),
               'titre': Textarea(attrs={
                    'class': 'form-titre',
                    'required': True
               }),
               'description': Textarea(attrs={
                    'class': 'form-desc',
                    'required': True
               }),
               'media': FileInput(attrs={
                    'class': 'form-media',
                    'required': True,
               }),
          }
          
          