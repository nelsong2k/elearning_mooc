from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Prefetch
from moviepy.video.io.VideoFileClip import VideoFileClip

from mooc.forms import ContactForm
from mooc.models import Formation, Cours, Contact
from .form import ContactHelpForm
from .models import *


# Create your views here.

def help_home(request):
    help = Helping.objects.all().order_by('-created_at')
    format = Formation.objects.all().order_by('-created_at')
    cours = Cours.objects.all().order_by('-created_at')
    return render(request, "indexhelp-login.html", {"formations": format, "cours": cours, "helps": help})


# ---------------------------------------------------------------------------------------------------------
class AddContactView(LoginRequiredMixin, CreateView):
    model = ContactHelp
    form_class = ContactHelpForm
    template_name = "contact.html"
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Le message a été envoyé avec succès.")
        return response


# -------------------------------------------------------------------------------------------------------------------------------
def support(request):
    return render(request, "support.html")


# ---------------------------------------------------------------------------------------------------------------------------
def maintenance(request):
    return render(request, "maintenance.html")


# --------------------------------------------------------------------------------------------------------------------------------------
def itsoftware(request):
    return render(request, "itsoftware.html")


# ----------------------------------------------------------------------------------------------------------------------------------------------
def mjs(request):
    return render(request, "mjs.html")


# --------------------------------------------------------------------------------------------------------------------------------------
def formations(request):
    return render(request, "formations.html")


# --------------------------------------------------------------------------------------------------------------------------------------
def maint_corrective(request):
    return render(request, "maint_corrective.html")


# --------------------------------------------------------------------------------------------------------------------------------------
class HelpListView(LoginRequiredMixin, ListView):
    model = Helping
    template_name = "help.html"
    paginate_by = 20  # if pagination is desired

    def get_queryset(self):
        return Helping.objects.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# ---------------------------------------------------------------------------------------------------------

def search_help(request):
    query = request.GET["search"]
    list_help = Helping.objects.filter(nom_helping__icontains=query)
    return render(request, 'search_help.html', {"list_help": list_help})


# ---------------------------------------------------------------------------------------------------------
class HelpDetailView(LoginRequiredMixin, DetailView):
    model = Helping
    template_name = "detail-help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_file = context['object'].files.first().file.path
        video_clip = VideoFileClip(video_file)
        duration = int(video_clip.duration)
        minutes, seconds = divmod(duration, 60)
        context['duration'] = '{:02d}:{:02d}'.format(minutes, seconds)

        # Ajouter la liste de Helping au contexte
        context['helping_list'] = Helping.objects.all().order_by('-created_at')

        return context
