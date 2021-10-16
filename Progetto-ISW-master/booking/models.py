from typing import Any

from django.db import models
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

# Create your models here.

class Hotel(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.CharField(max_length=100)
    citta = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=100)
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.nome



class Camera(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    posti_letto = models.PositiveIntegerField()
    servizi = models.TextField()

    def __str__(self):
        return "Stanza " + str(self.numero) + " dell'Hotel " + str(self.hotel)

    class Meta:
        verbose_name_plural = "camere"


class Prenotazione(models.Model):
    email = models.EmailField(max_length=100)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()

    def __str__(self):
        return "Prenotazione di " + str(self.email) + " nella " + str(self.camera)

    class Meta:
        verbose_name_plural = "prenotazioni"