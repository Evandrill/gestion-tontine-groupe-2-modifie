from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Formulaire de création d’utilisateur avec mot de passe sécurisé
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'telephone',
            'adresse',
        )

# Formulaire de modification d’un utilisateur (ex: dans admin ou profil)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'telephone',
            'adresse',
            'is_active',
            'is_staff',
        )
