from django import forms
from .models import Question, Choice, Comment
from profiles.models import Profile

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

# class Profile(profiles.models.Model):
#     class Meta:
#         model = Profil
#         fields = ['bild']