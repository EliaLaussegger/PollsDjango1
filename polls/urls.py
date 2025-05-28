from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("popular_feed/", views.PopularView.as_view(), name="popular_feed"),
    path("latest_feed/", views.LatestFeedView.as_view(), name="latest_feed"),
    path("every_feed/", views.EveryFeedView.as_view(), name="every_feed"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("new/", views.add_question, name="add_question"),
    path('<int:question_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', views.like, name='like'),
    path('impressum/', views.ImpressumView.as_view(), name='impressum'),
    path("<int:question_id>/like_question/", views.like_question, name="like_question"),
    path("logout/", views.logout_view, name="logout"),

]