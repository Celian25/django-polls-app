from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index_page"),
    path("results/", views.ResultsListView.as_view(), name="results_list_page"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail_page"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results_page"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
