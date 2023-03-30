from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

def chemin_du_fichier_memoire(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

User = get_user_model()

# Create your models here.
class Utilisateur(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     user_id = models.IntegerField()
     photo_profile = models.ImageField(upload_to='images/', blank=True) # configure path

     class Meta:
          abstract = True


class Administrateur(Utilisateur):
     titre = models.CharField(max_length=128)
     
     class Meta:
          db_table = 'admin'

     def __str__(self):
          return f'{super().user.first_name} {super().user.last_name} : {self.titre}'


class Theme(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     libelle = models.CharField(max_length=128, unique=True)
     
     class Meta:
          db_table = 'theme'
          
     def __str__(self):
          return f'{self.libelle}'


class Etablissement(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     libelle = models.CharField(max_length=128, unique=True)
    
     class Meta:
         db_table = 'etablissement'
    
     def __str__(self):
         return f'{self.libelle}'

     
class Parcours(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     libelle = models.CharField(max_length=128)
     etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
     adminstrateur = models.ForeignKey(Administrateur, on_delete=models.CASCADE)

     class Meta:
          db_table = 'parcours'
     
     def __str__(self):
          return f'{self.libelle}'

class Etudiant(Utilisateur):
     no_carte = models.BigIntegerField(unique=True)
     parcours = models.ForeignKey(Parcours, on_delete=models.CASCADE)
     deposer = models.BooleanField(default=False)

     class Meta:
          db_table = 'etudiant'

     def __str__(self):
          return f'{self.no_carte} {super().user.first_name} {super().user.last_name}'


class Memoire(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     num_ordre = models.CharField(max_length=128)
     titre = models.TextField()
     description = models.TextField()
     media = models.FileField(upload_to='documents/') # TODO: configure file path
     created_at = models.DateTimeField(auto_now_add=True)

     etudiant = models.OneToOneField(Etudiant, on_delete=models.CASCADE)

     theme = models.ForeignKey(Theme, on_delete=models.CASCADE)

     class Meta:
          db_table = 'memoire'
          ordering = ['created_at', 'num_ordre']

     def __str__(self):
          return f'{self.num_ordre} {self.titre}'
