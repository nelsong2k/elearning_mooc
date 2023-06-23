from django import forms
from mooc.models import *


class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['nom_formation', 'description', 'img']
        labels = {'nom_formation': 'Nom formation', 'description': 'Description', 'img': 'Image'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_formation'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['img'].widget.attrs.update({'class': 'form-control'})


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['formation', 'nom_cours', 'description_cours', 'full_description', 'image', 'date_fin']
        labels = {'formation': 'Formation', 'description': 'Description', 'nom_cours': 'Nom cours',
                  'description_cours': 'Description cours', 'full_description': 'Full description', 'image': 'image',
                  'date_fin': 'Date fin'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['formation'].widget.attrs.update({'class': 'form-control'})
        self.fields['nom_cours'].widget.attrs.update({'class': 'form-control'})
        self.fields['description_cours'].widget.attrs.update({'class': 'form-control'})
        self.fields['full_description'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_fin'].widget.attrs.update({'class': 'form-control', })


# ----------------------------------------------------------------------------------------------------------------------------------------

class TutorielForm(forms.ModelForm):
    class Meta:
        model = Tutoriel
        fields = ['cours', 'video', 'description', 'durer']
        labels = {'cours': 'Cours', 'video': 'Video', 'description': 'Description', 'durer': 'Durer'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cours'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['durer'].widget.attrs.update({'class': 'form-control'})


# ----------------------------------------------------------------------------------------------------------------------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(label="Nom utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
