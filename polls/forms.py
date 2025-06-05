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



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']