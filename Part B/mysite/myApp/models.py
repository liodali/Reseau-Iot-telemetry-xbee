from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cin = models.IntegerField(unique=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")

    def __str__(self):
        return "Profil de {}".format(self.user.username)


class Utilisateur(models.Model):
    personne = models.OneToOneField(Profil)

    def __str__(self):
        return "L\'utilisateur {}".format(self.personne.user.username)
