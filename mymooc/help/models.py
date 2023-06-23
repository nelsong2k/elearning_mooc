from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Helping(models.Model):
    nom_helping = models.CharField(max_length=200)
    desc_helping = models.CharField(max_length=200)
    image = models.ImageField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_helping


# -------------------------------------------------------------------------------------------

class Files(models.Model):
    helping = models.ForeignKey(Helping, related_name="files", on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField()
    description = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file} / {self.description}"
