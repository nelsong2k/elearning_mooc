import os

from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from moviepy.editor import VideoFileClip

from help.models import Helping
from .forms import *

User = get_user_model()


def home(request):
    help = Helping.objects.all().order_by('-created_at')
    format = Formation.objects.all().order_by('-created_at')
    cours = Cours.objects.all().order_by('-created_at')
    return render(request, "index.html", {"formations": format, "cours": cours, "helps": help})


# ----------------------------------------------------------------------------------------------------


@login_required
def home_login(request):
    help = Helping.objects.all().order_by('-created_at')
    format = Formation.objects.all().order_by('-created_at')
    cours = Cours.objects.all().order_by('-created_at')
    return render(request, "index-login.html", {"formations": format, "cours": cours, "helps": help})


# ------------------------------------------------------------------------------------------------------------
class AddContactView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact_login.html"
    success_url = "contact_login"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Le message a été envoyé avec succès.")
        return response


# ----------------------------------------------------------------------------------------------------
class AddContactIndexView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact_index.html"
    success_url = "contact_index"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Le message a été envoyé avec succès.")
        return response


# ----------------------------------------------------------------------------------------------------
class FormationListView(LoginRequiredMixin, ListView):
    model = Formation
    template_name = "formation.html"
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(num_cours=Count('cours'))
        return queryset


# ----------------------------------------------------------------------------------------------------

class CoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = "cours.html"
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['formations'] = Formation.objects.annotate(num_cours=Count('cours'))
        return context

    def get_queryset(self):
        # Récupérer les cours dont la date de fin est ultérieure à la date et à l'heure actuelles
        queryset = super().get_queryset()
        now = timezone.now()
        queryset = queryset.filter(date_fin__gt=now).order_by('-created_at')
        return queryset


# ----------------------------------------------------------------------------------------------------
class CoursDetailView(DetailView):
    model = Cours
    template_name = "detail-cours.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cours = self.get_object()

        # Ajouter la durée de disponibilité du cours au contexte
        disponibilite = cours.date_fin - cours.created_at.date()
        context['disponibilite'] = disponibilite.days

        # Ajouter la liste des user qui se sont inscrit au cours au contexte
        user_suivre = User.objects.filter(suivre__cours=cours)
        context['user_suivre'] = user_suivre

        # Ajouter la liste des utilisateurs qui ont participé aux quiz du cours et leurs scores au contexte
        quiz_cours = Quiz.objects.filter(cours=cours)
        user_quiz_scores = []
        for quiz in quiz_cours:
            for result in quiz.result_set.all():
                if result.user:
                    score = result.score
                    required_score = quiz.required_score_to_pass
                    pass_status = ""
                    if score < required_score:
                        pass_status = "Échoué"
                    else:
                        pass_status = "Réussi"
                    user_quiz_scores.append({
                        'user': f"{result.user.first_name} {result.user.last_name}",
                        'score': score,
                        'heure': result.created.strftime('%Y-%m-%d %H:%M:%S'),
                        'pass_status': pass_status,
                        'quiz': quiz
                    })
        # Trier la liste des résultats des quiz par heure décroissante
        user_quiz_scores = sorted(
            user_quiz_scores, key=lambda x: x['heure'], reverse=True)
        context['user_quiz_scores'] = user_quiz_scores

        # Ajouter la liste des cours au contexte
        context['cours_list'] = Cours.objects.all().order_by('-created_at')

        return context


# ----------------------------------------------------------------------------------------------------

class TutorielDetailView(LoginRequiredMixin, DetailView):
    model = Tutoriel
    template_name = "detail-video.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()

        return context

    def post(self, request, *args, **kwargs):
        tutoriel = self.get_object()
        try:
            TutorielLike.objects.create(user=request.user, tutoriel=tutoriel)
        except IntegrityError:
            TutorielLike.objects.filter(
                user=request.user, tutoriel=tutoriel).delete()
        return redirect('detail-video', pk=tutoriel.pk)


# ------------------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------

def addSuivre(request, pk):
    user: User = User.objects.get(pk=request.user.id)
    cours = Cours.objects.get(pk=pk)
    user.cours_set.add(cours)

    return redirect(reverse_lazy('list_suivres', kwargs={'pk': pk}))


# ----------------------------------------------------------------------------------------------------

class SuivreListView(LoginRequiredMixin, ListView):
    model = Suivre
    template_name = 'suivre.html'

    def get_queryset(self):
        # Filtre les objets Suivre en fonction de l'utilisateur connecté
        return Suivre.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupère les cours suivis par l'utilisateur
        cours_suivis = [suivre.cours for suivre in self.object_list]
        context['cours_suivis'] = cours_suivis

        # Récupère le nombre de cours sur la plateforme
        context['nb_cours'] = Cours.objects.count()
        return context


# ----------------------------------------------------------------------------------------------------

class AddUser(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "register.html"
    success_url = "login"

    def form_valid(self, form):
        # Crypter le mot de passe avant de l'enregistrer
        form.instance.password = make_password(form.cleaned_data['password'])

        # Vérifier si tous les champs nécessaires sont remplis
        if not form.cleaned_data['username'] or not form.cleaned_data['email'] or not form.cleaned_data['last_name'] \
                or not form.cleaned_data['first_name'] or not form.cleaned_data['password']:
            messages.error(self.request, "Veuillez remplir tous les champs.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        messages.success(
            self.request, "Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter.")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        errors = form.errors.as_data()

        for field, error_list in errors.items():
            for error in error_list:
                if field == 'username' and error.code == 'unique':
                    messages.error(
                        self.request, "Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
                else:
                    # Afficher le nom du champ qui n'a pas été rempli
                    if error.code == 'required':
                        field_name = form.fields[field].label
                        messages.error(
                            self.request, f"Le champ '{field_name}' est obligatoire.")
                    else:
                        messages.error(self.request, error)

        return response


# ----------------------------------------------------------------------------------------------------


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('choix')
            else:
                messages.error(request, "Authentification échouée")

                return render(request, 'login.html', {'form': form})
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'

            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


# ----------------------------------------------------------------------------------------------------
def logout_user(request):
    logout(request)
    return redirect('home')


# ----------------------------------------------------------------------------------------------------

class QuizDetailView(DetailView):
    model = Quiz
    template_name = "quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# ----------------------------------------------------------------------------------------------------


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
    })


# ----------------------------------------------------------------------------------------------------

def save_quiz_view(request, pk):
    # print(request.POST)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        mutiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            print('selected', a_selected)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append(
                    {str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * mutiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})


# ----------------------------------------------------------------------------------------------------


def deletesuivre(request, pk):
    user: User = User.objects.get(pk=request.user.id)
    cours = Cours.objects.get(pk=pk)
    user.cours_set.remove(cours)

    return redirect(reverse_lazy('list_suivres', kwargs={'pk': pk}))


# ---------------------------------------------------------------------------------------

def choix(request):
    return render(request, "choix.html")


# ---------------------------------------------------------------------------------------------------------------------

def search(request):
    query = request.GET["search"]
    list_cours = Cours.objects.filter(nom_cours__icontains=query)
    return render(request, 'search.html', {"list_cours": list_cours})


# --------------------------------------------------------------------------------------------------------------------

class ProfilDetailView(DetailView):
    model = User
    template_name = "profil.html"
    success_url = 'profil'


# --------------------------------------------------------------------------------------------------------------------

class CoursSuivisView(LoginRequiredMixin, ListView):
    model = Suivre
    template_name = 'cours_suivis.html'
    success_url = 'cours_suivis'

    def get_queryset(self):
        # Filtre les objets Suivre en fonction de l'utilisateur connecté
        return Suivre.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupère les cours suivis par l'utilisateur
        cours_suivis = [suivre.cours for suivre in self.object_list]
        context['cours_suivis'] = cours_suivis
        return context


# -------------------------------------------------------------------------------------------------------

def deleteCoursSuivis(request, pk):
    user: User = User.objects.get(pk=request.user.id)
    cours = Cours.objects.get(pk=pk)
    user.cours_set.remove(cours)

    return redirect(reverse_lazy('cours_suivis', kwargs={'pk': pk}))


# -------------------------------------------------------------------------------------------------------


def reglageCompte(request):
    if not request.user.is_authenticated:
        # Redirect the user to the login page if they are not authenticated
        return redirect('login')

    user = request.user  # Get the authenticated user
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        # Add other fields here
    }
    form = UserForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        # Save the user's changes
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.username = form.cleaned_data['username']
        user.email = form.cleaned_data['email']
        user.password = make_password(form.cleaned_data['password'])
        user.pwd_confirm = make_password(form.cleaned_data['pwd_confirm'])
        user.save()

        # Redirect to the profile page
        return redirect(reverse('reglage-compte'))

    context = {'form': form}
    return render(request, 'reglage.html', context)


# --------------------------------------------------------------------------------------------------------------------------------------------------
class UserResultsView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = 'user_results.html'
    context_object_name = 'cours_with_results'

    def get_queryset(self):
        # Récupérer tous les résultats de quiz de l'utilisateur connecté
        user_results = Result.objects.filter(user=self.request.user)

        # Créer un dictionnaire pour stocker les cours et les résultats de quiz associés
        cours_with_results = {}

        # Ajouter chaque résultat de quiz à la liste de résultats correspondant au cours correspondant
        for result in user_results:
            quiz = result.quiz
            cours = quiz.cours

            if cours in cours_with_results:
                cours_with_results[cours].append({
                    'result': result.score,
                    'heure': result.created.strftime('%d-%m-%Y   %H:%M:%S'),
                })
            else:
                cours_with_results[cours] = [{
                    'result': result.score,
                    'heure': result.created.strftime('%d-%m-%Y %H:%M:%S'),
                }]

        # Retourner la liste des cours avec les résultats de quiz associés
        return cours_with_results.items()


# ------------------------------------------------------------------------------------------------------------------------------------
class ForumDetailView(DetailView):
    model = Cours
    template_name = "forum.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cours = self.get_object()

        # Ajouter la durée de disponibilité du cours au contexte
        disponibilite = cours.date_fin - cours.created_at.date()
        context['disponibilite'] = disponibilite.days

        # Ajouter la liste des user qui se sont inscrit au cours au contexte
        user_suivre = User.objects.filter(suivre__cours=cours)
        context['user_suivre'] = user_suivre

        # Ajouter la liste des utilisateurs qui ont participé aux quiz du cours et leurs scores au contexte
        quiz_cours = Quiz.objects.filter(cours=cours)
        user_quiz_scores = []
        for quiz in quiz_cours:
            for result in quiz.result_set.all():
                if result.user:
                    score = result.score
                    required_score = quiz.required_score_to_pass
                    pass_status = ""
                    if score < required_score:
                        pass_status = "Échoué"
                    else:
                        pass_status = "Réussi"
                    user_quiz_scores.append({
                        'user': f"{result.user.first_name} {result.user.last_name}",
                        'score': score,
                        'heure': result.created.strftime('%Y-%m-%d %H:%M:%S'),
                        'pass_status': pass_status,
                        'quiz': quiz
                    })
        # Trier la liste des résultats des quiz par heure décroissante
        user_quiz_scores = sorted(
            user_quiz_scores, key=lambda x: x['heure'], reverse=True)
        context['user_quiz_scores'] = user_quiz_scores

        # Ajouter la liste des cours au contexte
        context['cours_list'] = Cours.objects.all().order_by('-created_at')

        return context


# ----------------------------------------------------------------------------------------------------------------------------------------------
class FormationDetailView(ListView):
    model = Cours
    template_name = "detail-formation.html"
    context_object_name = "cours"
    paginate_by = 30

    def get_queryset(self):
        formation = Formation.objects.get(pk=self.kwargs['pk'])
        return formation.cours_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formation'] = Formation.objects.get(pk=self.kwargs['pk'])
        return context


# ---------------------------------------------------------------------------------------------------------------------------------
class AllCoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = "allcours.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
        # Récupérer les cours dont la date de fin est ultérieure à la date et à l'heure actuelles
        queryset = super().get_queryset()
        now = timezone.now()
        queryset = queryset.filter(date_fin__gt=now).order_by('-created_at')
        return queryset
