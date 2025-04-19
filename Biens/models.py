import datetime
from django.db import models
from django.contrib.auth.models import User



class Categories(models.Model):
    name= models.CharField(max_length=250)
    
    def __str__(self):
        return self.name

# # class pour les biens 

class Biens(models.Model):
    
    nom = models.CharField(max_length= 100)
    type = models.ForeignKey(Categories, on_delete=models.CASCADE, default='Terrain')
    date_operateur_ajout= models.DateTimeField(auto_now_add=True)
    proprietaire = models.CharField(max_length=50)
    image = models.ImageField(upload_to="images/",null=True,blank=True)
    dimension = models.CharField(max_length=10)
    document = models.FileField(upload_to="PDF", null=True, blank=True)
    adresse = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    date_operateur_modification = models.DateTimeField(auto_now=True)
    modifie_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='biens_modifies')  # Dernière personne qui a modifié
    
    est_supprimer = models.BooleanField(default=False)  # Ajout du champ pour la corbeille
    date_operateur_supprimer = models.DateTimeField(null=True, blank=True)


    def supprimer(self):
        # Marque le bien comme supprimé sans le supprimer définitivement."""
        self.est_supprimer = True
        self.date_operateur_supprimer = datetime.datetime.now()
        self.save()

    def restaurer(self):
        # Restaure un bien supprimé."""
        self.est_supprimer = False
        self.date_operateur_supprimer = None
        self.save()
    
    class Meta:
        ordering =['-date_operateur_ajout']

    
# # Create your models here.
