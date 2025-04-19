from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.timezone import now

def renomer_image(instance, filename):
    ext = filename.split('.')[-1]  # Récupération de l'extension de fichier
    if instance.user.username:
        filename =f"{instance.user.username}.{ext}" # Nom personnalisé
    return os.path.join('image/photo_profile/', filename)  # Stocke dans 'media/image/photo_profile/'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.IntegerField(null=True, blank=True)
    photo_profile = models.ImageField(upload_to=renomer_image, blank=True)
    etat_connexion = models.DateTimeField(default=now)  # Correction du nom de la variable

    def is_online(self):
        return (now() - self.etat_connexion).seconds < 300  # 5 minutes d'inactivité

    def __str__(self):
        return self.user.username
    
class Permission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ajouter = models.BooleanField(default=False)
    modifier = models.BooleanField(default=False)
    supprimer = models.BooleanField(default=False)

    def __str__(self):
        return f"Permissions de {self.user.username}"