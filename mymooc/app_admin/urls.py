from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("list_formation", list_formation, name="list_formation"),
    path("ajouter-formation", AddFormation.as_view(), name="ajouter-formation"),
    path("list_cours", list_cours, name="list_cours"),
    path("ajouter-cours", AddCours.as_view(), name="ajouter-cours"),
    path("list_tutoriel", list_tutoriel, name="list_tutoriel"),
    path("ajouter-tutoriel", AddTutoriel.as_view(), name="ajouter-tutoriel"),
    path("update-formation/<int:pk>", UpdateFormation.as_view(), name="update-formation"),
    path("delete-formation/<int:pk>", DeleteFormation.as_view(), name="delete-formation"),
    path("update-cours/<int:pk>", UpdateCours.as_view(), name="update-cours"),
    path("delete-cours/<int:pk>", DeleteCours.as_view(), name="delete-cours"),
    path("update-tutoriel/<int:pk>", UpdateTutoriel.as_view(), name="update-tutoriel"),
    path("delete-tutoriel/<int:pk>", DeleteTutoriel.as_view(), name="delete-tutoriel"),

]
