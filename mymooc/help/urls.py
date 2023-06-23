from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path("help-home", help_home, name="help-home"),
    path("list-help", HelpListView.as_view(), name="list-help"),
    path("contact/", contact, name="contact"),
    path("recherche_help", search_help, name="search_help"),
    # path("files/<int:pk>/", FileDetailView.as_view(), name="files"),
    # path("helping/<int:pk>/", HelpingDetailView.as_view(), name="helping"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
