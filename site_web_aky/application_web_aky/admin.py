from django.contrib import admin

from .models import (
    Administrateur,
    Etudiant,
    Memoire,
    Theme,
    Etablissement,
    Parcours,
)

admin.site.register(Etablissement)
admin.site.register(Etudiant)
admin.site.register(Administrateur)
admin.site.register(Memoire)
admin.site.register(Theme)
admin.site.register(Parcours)
