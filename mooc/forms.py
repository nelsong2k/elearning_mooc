from django import forms
from .models import *


class PostulantForm(forms.ModelForm):
    class Meta:
        model = Postulant
        fields = ['nom', 'email', 'confirm_pwd']
        labels = {'nom': 'Nom complet', 'confirm_pwd': 'Confirmation de mot de passe'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_pwd'].widget.attrs.update({'class': 'form-control'})


# -------------------------------------------------------------------------------------------------------------------
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'username', 'password']
        labels = {'last_name': 'Nom ', 'first_name': 'Prenom', 'email': 'Email', 'username': 'Nom utilisateur',
                  'password': 'Mot de passe'}
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'type': 'password'})


# -------------------------------------------------------------------------------------------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(label="Nom utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# -------------------------------------------------------------------------------------------------------------------

class UserForm(forms.Form):
    last_name = forms.CharField(label="Nom de famille", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Nom utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Nouveau Mot de passe",
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pwd_confirm = forms.CharField(label="Mot de passe de confirmation",
                                  widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# ----------------------------------------------------------------------------------------------------------------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'objet', 'message']
        labels = {'name': 'Nom ', 'email': 'Email', 'objet': 'Objet', 'message': 'Message'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['objet'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
