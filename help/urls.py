from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *


urlpatterns = [
    path("help-home", help_home, name="help-home"),
    path("list-help", HelpListView.as_view(), name="list-help"),
    path("contact/", AddContactView.as_view(), name="contact"),
    path("recherche_help", search_help, name="search_help"),
    path("support", support, name="support"),
    path("maintenance-preventive", maintenance, name="maintenance"),
    path('it-software', itsoftware, name="itsoftware"),
    path('mise-jour-securite', mjs, name="mjs"),
    path('formations', formations, name="formations"),
    path('maintenance-corrective', maint_corrective, name="maint_corrective"),
    path("detail-help/<int:pk>", HelpDetailView.as_view(), name="detail-help"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
