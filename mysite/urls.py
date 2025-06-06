from django.contrib import admin
from django.urls import include, path
from polls import views as views_polls
from mysite import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path('users/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('impressum/', views.ImpressumView.as_view(), name='impressum'),
    path('', views.home_redirect_view, name='home'),
    path("<str:user_id>/", views_polls.vote, name="vote"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)