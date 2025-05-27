from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    else:
        return redirect('accounts:index')
    


class ImpressumView(TemplateView):
    template_name = "polls\templates\polls\impressum.html"