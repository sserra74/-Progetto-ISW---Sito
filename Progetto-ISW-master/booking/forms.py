from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Camera

from .models import *


from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control", 'id':"exampleInputEmail1", 'aria-describedby':"emailHelp", 'placeholder':"Inserisci Email", 'name':"email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control", 'id':"exampleInputPassword1", 'placeholder':"Password", 'name':"password"}))
    confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control", 'id':"exampleInputPasswordConferma", 'placeholder':"Conferma Password"}))
    nome = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"nameUtente", 'placeholder': "Nome", 'name':"nome"}))
    cognome = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"cognomeUtente", 'placeholder': "Cognome", 'name':"cognome"}))

    class Meta:
        model = User
        fields = ("email", "password", "confirmpassword", "nome", "cognome")

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['email'], email=self.cleaned_data['email'], password=self.cleaned_data['password'])
        user.first_name = self.cleaned_data['nome']
        user.last_name = self.cleaned_data['cognome']
        user.save()
        return user


class AddHotelForm(forms.Form):
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "Nome", 'placeholder': "Nome", 'name': "nome"}))
    descrizione = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "Descrizione", 'placeholder': "Descrizione", 'name': "descrizione"}))
    citta = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "Citta", 'placeholder': "Citta", 'name': "citta"}))
    indirizzo = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'id': "Indirizzo", 'placeholder': "Indirizzo", 'name': "indirizzo"}))

    class Meta:
        model = Hotel
        fields = ("nome", "descrizione", "citta", "indirizzo")




class SearchForm(forms.Form):
    citta = forms.CharField(widget=forms.TextInput(
        attrs={'class':"form-control", 'placeholder':"Citta", 'id':"citySearch", 'name':"city"}))
    postiletto = forms.CharField(widget=forms.NumberInput(
        attrs={'class': "form-control", 'placeholder': "Numero Persone", 'id': "nPersSearch", 'name': "size"}))
    checkin = forms.CharField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': "form-control", 'placeholder': "Dal", 'id': "fromSearch", 'name': "checkin"}))
    checkout = forms.CharField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': "form-control", 'placeholder': "Al", 'id': "toSearch", 'name': "checkout"}))


class AddCameraForm(forms.Form):
    numero = forms.IntegerField(widget=forms.NumberInput(attrs = {'type':"Number", 'class':"form-control", 'id':"Numero", 'placeholder':"Numero", 'name':"numero"}))
    posti_letto = forms.IntegerField(widget=forms.NumberInput(attrs = {'type':"Text", 'class':"form-control", 'id':"Posti", 'placeholder':"Posti", 'name':"posti"}))
    servizi = forms.CharField(widget=forms.TextInput(attrs={'type':"Text",'class':"form-control",'id':"Servizi",'name':"servizi",'placeholder':"Wifi, Tv, Climatizzatore, Minifrigo"}))

    class Meta:
        model = Camera
        fields = ("numero", "posti_letto", "servizi")

    def save(self, hotel):
        camera = Camera.objects.create(hotel=hotel, numero=self.cleaned_data['numero'], posti_letto=self.cleaned_data['posti_letto'], servizi=self.cleaned_data['servizi'])
        camera.save()
        return camera

class LoginUserForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control", 'id':"exampleInputEmail1", 'aria-describedby':"emailHelp", 'placeholder':"Inserisci Email", 'name':"email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control", 'id':"exampleInputPassword1", 'placeholder':"Password", 'name':"password"}))
