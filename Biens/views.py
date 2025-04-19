from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import FileResponse, Http404

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView

from Utilisateurs.models import Permission
from .forms import *

from django.contrib import messages
from datetime import datetime
from django.http import FileResponse

from .models import *


from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def telecharger_document(request, biens_id):
    biens = get_object_or_404(Biens, id=biens_id)

    if biens.document:
        response = FileResponse(biens.document.open(), as_attachment=True)
        return response
    else:
        raise Http404("Document non trouvé")
    
# # Class dj'ajout des données

class Affichage(LoginRequiredMixin, ListView):
    context_object_name = 'biens'
    # Affichage du template
    model = Biens
    template_name = 'biens.html'
    
    # Récupération des données
    def get_queryset(self):
        return Biens.objects.filter(est_supprimer=False)  # Afficher uniquement les biens actifs

@login_required(login_url='login')
def recherche(request):

    query = request.GET.get('biens')
    donnees= Biens.objects.filter(nom__icontains=query)
    context = {
        'donnees' : donnees
    }
    return render(request, 'resultat_recheche.html', context)

class AjoutBiens(LoginRequiredMixin, CreateView):

    # utilisation du modele
    model = Biens
    # specifier le forulaire à utiliser
    form_class = formBiens
    # afichage du template
    template_name = 'ajout_biens.html'
    # redirection après enregistrement 
    success_url = reverse_lazy('Biens:biens') 


   
# Vue pour "supprimer" un bien (envoyer en corbeille)
class delete(LoginRequiredMixin, UpdateView):
    model = Biens
    fields = []  # Aucun formulaire, on modifie juste l'état du bien
    template_name = "delete.html"

    def form_valid(self, form):
        Biens = self.get_object()
        Biens.supprimer()  # Marque le bien comme supprimé
        return redirect('Biens:biens')  # Redirection vers la liste des biens

class CorbeilleListView(LoginRequiredMixin, ListView):
    model = Biens
    template_name = "corbeille.html"
    context_object_name = "biens"

    def get_queryset(self):
        return Biens.objects.filter(est_supprimer=True)  # Afficher uniquement les biens supprimés

def restaurer_bien(request, biens_id):
    biens = get_object_or_404(Biens, id=biens_id, est_supprimer=True)
    biens.restaurer()
    messages.success(request, "Le Bien a été Restorer avec Succes!")
    return redirect('Biens:corbeille')  # Redirection vers la liste des biens

    # return JsonResponse({"message": f"Le bien '{biens.nom}' a été restauré avec succès."})

class Supprimer(LoginRequiredMixin, DeleteView):
    model = Biens
    template_name = "deleteDef.html"
    success_url = reverse_lazy('Biens:corbeille')

# class pour la modification


class update_donnees(LoginRequiredMixin, UpdateView):

    # recuperation du model
    model = Biens
    # specifier le formulaire
    form_class = formBiens
    # princision du templates
    template_name = 'modifierBiens.html'
    # redirection

    def form_valid(self, form):
        Biens = form.save(commit=False)
        Biens.modifie_par = self.request.user  # Enregistre l'utilisateur qui modifie
        Biens.save()
        return super().form_valid(form)
     
    success_url = reverse_lazy('Biens:biens')


    # def get_success_url(self):
    #     """ Redirige après la modification """
    #     return reverse_lazy('detailBiens', kwargs={'pk': self.object.pk})


class edit(LoginRequiredMixin, DetailView):

    model = Biens
    template_name = 'detailBiens.html'
    context_object_name = 'n'