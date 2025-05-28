from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Comment, Vote, Like
from django.urls import reverse_lazy
from .forms import QuestionForm, CommentForm
from django.forms import inlineformset_factory
from django.views.generic import TemplateView
from django.contrib import messages
from profiles.models import Profile
from functools import wraps


class ImpressumView(TemplateView):
    template_name = "polls/impressum.html"


class PopularView(generic.ListView):
    template_name = "polls/popular.html"
    context_object_name = "top_questions"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()) \
    .order_by('-likes', '-pub_date')[:5]



class IndexView(TemplateView):
    template_name = "polls/index.html"



class LatestFeedView(generic.ListView):
    template_name = "polls/latest_feed.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()) \
    .order_by('-pub_date')[:5]

class EveryFeedView(generic.ListView):
    template_name = "polls/every_feed.html"
    context_object_name = "all_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")

def check_loggedin(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('accounts:index')

        try:
            profile = user.profile
        except Profile.DoesNotExist:
            return redirect('accounts:verification')

        if not profile.is_verified:
            return redirect('accounts:verification')

        return view_func(request, *args, **kwargs)

    return _wrapped_view

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['comments_sorted'] = question.comment_set.order_by('-likes')
        return context
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



@check_loggedin
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        messages.error(request, "Du hast schon mal abgestimmt")

    existing_vote = Vote.objects.filter(author=request.user, question=question).first()
    if existing_vote:
        comments_sorted = question.comment_set.order_by('-likes')
        return render(request, "polls/detail.html", {
            "question": question,
            "comments_sorted": comments_sorted,
            "error_message": "Du hast schon mal abgestimmt",
        })

    selected_choice.votes = F("votes") + 1
    selected_choice.save()


    Vote.objects.create(author=request.user, question=question, choice=selected_choice)

    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
ChoiceFormSet = inlineformset_factory(Question, Choice, fields=['choice_text'], extra=3)
@check_loggedin
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            if request.user.is_authenticated:
                question.author = request.user
            question.save()
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('polls:index')
        else:
            formset = ChoiceFormSet()
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    return render(request, 'polls/add_question.html', {'form': form, 'formset': formset})

@check_loggedin
def add_comment(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.pub_date = timezone.now()
            if request.user.is_authenticated:
                comment.author = request.user
   
            comment.save()
            return redirect('polls:detail', pk=question.id)
    else:
        form = CommentForm()

    return render(request, 'polls/detail.html', {
        'question': question,
        'form': form,
    })



@check_loggedin
def like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    existing_like = Like.objects.filter(author=request.user, comment=comment).first()
    if existing_like:
        messages.error(request, "You have already liked this comment.")
    else:
        Like.objects.create(author=request.user, comment=comment)
        comment.likes += 1
        comment.save()
    return redirect('polls:detail', pk=comment.question.id)



@check_loggedin
def like_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    existing_like = Like.objects.filter(author=request.user, question=question).first()
    if existing_like:
        messages.error(request, "You have already liked this Question.")
    else:
        Like.objects.create(author=request.user, question=question)
        question.likes += 1
        question.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    return redirect('polls:detail', pk=question.id)


def logout_view(request):
    logout(request)
    request.session["email_sent"] = False 
    return redirect('accounts:index')
