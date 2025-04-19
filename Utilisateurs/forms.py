from django import forms 
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta():
        model = User
        fields=[
            
            'username',
            'password1',
            'password2',
            'is_active',
        ]
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    
                    'class':"input100" ,
                    'placeholder':"Nom Utilisateur"
                }
                
            ),

            'password1': forms.PasswordInput(
                attrs = {
                    
                    'class':"input100" ,
                    'placeholder':"Mot de passe",
                }
                
            ),

            'password2': forms.PasswordInput(
                attrs = {
                    
                    'class':"input100" ,
                    'placeholder':"Confirmer le mot de passe",
                }
                
            ),
            'is_active': forms.CheckboxInput(
                attrs = {
                    
                    'placeholder':"Confirmer le mot de passe",
                }
                
            )
          
          
        }
    
   
        
class ProfileForm(forms.ModelForm):


    class Meta():
        model = Profile
        fields = [
            
            'number',
            'photo_profile'
        ]

        widgets = {
            'number': forms.NumberInput(
                attrs = {
                    
                    'class':"input100" ,
                    'placeholder':"numero telephone"
                }
                
            ),

            'photo_profile': forms.FileInput(
               
                
            ),

        }