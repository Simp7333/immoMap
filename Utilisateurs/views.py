from django.shortcuts import render,redirect, get_object_or_404

from django.contrib.auth import login,authenticate, logout
from .forms import *

from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse



from django.views.generic import ListView

from django.contrib.auth.models import User
from .models import *

from .forms import ProfileForm, UserForm
import json
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from Biens.models import Biens , Categories
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class LocationListView(LoginRequiredMixin,ListView):
    model = Biens
    template_name = 'home.html'
    context_object_name = 'locations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locations = list(self.get_queryset().values('nom', 'latitude', 'longitude'))
        context['locations_json'] = mark_safe(json.dumps(locations))  # Éviter l'échappement HTML
       
       # Compter le nombre de biens par catégorie
        data = []
        for categorie in Categories.objects.all():
            count = Biens.objects.filter(type=categorie).count()  # "type" fait référence à "Categorie"
            data.append({"categorie": categorie.name, "count": count})
        
        context["data"] = data  # Ajouter au contexte pour affichage dans le template
        
        
        return context
    

class Affichage(LoginRequiredMixin, ListView):

    model = Profile  # Utilise model au lieu de queryset
    template_name = 'utilisateur.html'
    context_object_name = 'profils' 

@csrf_exempt
def permissions(request, user_id):
    """ Gère les permissions globales d'un utilisateur """
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        data = json.loads(request.body)
        permissions, _ = Permission.objects.get_or_create(user=user)
        permissions.ajouter = data.get("ajouter", False)
        permissions.modifier = data.get("modifier", False)
        permissions.supprimer = data.get("supprimer", False)
        permissions.save()
        return JsonResponse({"success": True})

    else:
        permissions, _ = Permission.objects.get_or_create(user=user)
        return render(request, "permission.html", {"user": user, "permissions": permissions})
    
def modifier_bien(request, bien_id):
    """ Vérifie si l'utilisateur a la permission de modifier un bien """
    bien = get_object_or_404(Biens, id=bien_id)
    user_permissions = Permission.objects.filter(user=request.user).first()

    if not user_permissions or not user_permissions.modifier:
        return JsonResponse({"error": "Vous n'avez pas la permission de modifier ce bien"}, status=403)

    # Logique pour modifier le bien ici
    return JsonResponse({"success": True})
#fonction pour creation de compte
def Creation_compte(request):
    registered = False
    if request.method == "POST":

        # Assure-toi de bien inclure request.FILES pour gérer les fichiers comme l'image de profil
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST, files=request.FILES)  # Ajouter 'files=request.FILES'

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

            # Envoi du message de succès après la création du compte
            messages.success(request, "Compte créé avec succès, connectez-vous maintenant.")
            return redirect("acount_login")

        else:
            messages.error (request, user_form.errors, profile_form.errors)

    else:
        messages.error(request, "Compte non créé.")
        user_form = UserForm()
        profile_form = ProfileForm()

    content = {
        'registered': registered,
        'form1': user_form,
        'form2': profile_form,
    }
    return render(request, "creation.html", content)


#fonction pour se connecter
def Connecter_compte(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('acc')
        # else:
        #     messages.error(request, "vous etes desactive")
        #     return redirect("acount_login")

        else:
            messages.error(request, "Nom d\'utilisateur ou mot de passe incorect.")
            return redirect("acount_login")
    return render(request, 'login.html')

def online_users(request):
    five_minutes_ago = now() - timedelta(minutes=5)
    online_users = User.objects.filter(profile__etat_connexion__gte=five_minutes_ago).values('id', 'username')

    return JsonResponse({'online_users': list(online_users)})

@csrf_exempt  # Désactive temporairement la vérification CSRF pour les tests (mieux d'utiliser un token CSRF en production)
def toggle_user_status(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        # Vérifie si l'utilisateur est un superutilisateur
        if user.is_superuser:
            return JsonResponse({"success": False, "message": "Vous ne pouvez pas désactiver un superutilisateur."}, status=403)
        
        user.is_active = not user.is_active  # Toggle du statut
        user.save()
        return JsonResponse({"success": True, "new_status": user.is_active})
    return JsonResponse({"success": False}, status=400)

# fonction pour la deconnection

@login_required(login_url='acount_login')
def Deconnection(request):

    logout(request)
    return redirect('acount_login')
