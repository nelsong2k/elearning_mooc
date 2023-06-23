from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from mooc.models import *
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .forms import *


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    nb_formations = Formation.objects.filter(user=user).count()
    nb_cours = Cours.objects.filter(user_cours=user).count()
    nb_tutoriels = Tutoriel.objects.filter(user=user).count()
    nb_quiz = Quiz.objects.filter(user=user).count()
    return render(request, "db.html",
                  {"nb_formations": nb_formations, "nb_cours": nb_cours, "nb_tutoriels": nb_tutoriels,
                   "nb_quiz": nb_quiz})


# -----------------------------------------------------------------------------------------------------------------------------------------------------
def list_formation(request):
    list_formation = Formation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'list_formation.html', {"list_formation": list_formation})


def list_cours(request):
    if not request.user.is_authenticated:
        return redirect('login')
    list_cours = Cours.objects.filter(user_cours=request.user).order_by('-created_at')
    return render(request, 'list_cours.html', {"list_cours": list_cours})


class AddFormation(CreateView):
    model = Formation
    form_class = FormationForm
    template_name = "add-formation.html"
    success_url = "list_formation"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AddCours(CreateView):
    model = Cours
    form_class = CoursForm
    template_name = "add-cours.html"
    success_url = "list_cours"

    def form_valid(self, form):
        form.instance.user_cours = self.request.user
        return super().form_valid(form)


def list_tutoriel(request):
    list_tutoriel = Tutoriel.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'list_tutoriel.html', {"list_tutoriel": list_tutoriel})


class AddTutoriel(LoginRequiredMixin, CreateView):
    model = Tutoriel
    form_class = TutorielForm
    template_name = "add-tutoriel.html"
    success_url = "list_tutoriel"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateFormation(LoginRequiredMixin, UpdateView):
    model = Formation
    form_class = FormationForm
    template_name = 'update-formation.html'
    success_url = "/my-admin/list_formation"


class DeleteFormation(DeleteView):
    model = Formation
    template_name = 'delete-formation.html'
    success_url = "/my-admin/list_formation"


class UpdateCours(LoginRequiredMixin, UpdateView):
    model = Cours
    form_class = CoursForm
    template_name = 'update-cours.html'
    success_url = "/my-admin/list_cours"


class DeleteCours(DeleteView):
    model = Cours
    template_name = 'delete-cours.html'
    success_url = "/my-admin/list_cours"


class UpdateTutoriel(LoginRequiredMixin, UpdateView):
    model = Tutoriel
    form_class = TutorielForm
    template_name = 'update-tutoriel.html'
    success_url = "/my-admin/list_tutoriel"


class DeleteTutoriel(DeleteView):
    model = Tutoriel
    template_name = 'delete-tutoriel.html'
    success_url = "/my-admin/list_tutoriel"
