from django import forms
from .models import Question, Choice, Comment
from profiles.models import Profile

class Profile(profiles.models.Model):
    class Meta:
        model = Profil
        fields = ['bild']