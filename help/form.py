from django import forms

from help.models import ContactHelp


class ContactHelpForm(forms.ModelForm):
    class Meta:
        model = ContactHelp
        fields = ['name', 'email', 'objet', 'message']
        labels = {'name': 'Nom ', 'email': 'Email', 'objet': 'Objet', 'message': 'Message'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['objet'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})