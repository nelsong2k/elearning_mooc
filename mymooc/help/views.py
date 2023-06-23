from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.db.models import Prefetch

from .models import *


# Create your views here.

def help_home(request):
    return render(request, "indexhelp-login.html")


# ---------------------------------------------------------------------------------------------------------
def contact(request):
    return render(request, "contact.html")


# ---------------------------------------------------------------------------------------------------------


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

# class FileDetailView(DetailView):
#     model = Files
#     template_name = "files.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
