from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("choix", choix, name="choix"),
    path("home-login", home_login, name="home-login"),
    path('detail_cours/<int:pk>', CoursDetailView.as_view(), name='detail-cours'),
    path('cours_list', CoursListView.as_view(), name='cours_list'),
    path('detail_video/<int:pk>', TutorielDetailView.as_view(), name='detail-video'),
    path('register', AddUser.as_view(), name='register'),
    path('login', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('suivre/add/<int:pk>', addSuivre, name='add_suivre'),
    path('list_suivres/<int:pk>', SuivreListView.as_view(), name='list_suivres'),
    path('quiz-view/<int:pk>/', QuizlDetailView.as_view(), name='quiz-view'),
    path('quiz-view/<int:pk>/data/', quiz_data_view, name='quiz-data-view'),
    path('quiz-view/<int:pk>/save', save_quiz_view, name='save-view'),
    path('suivre/delete/<int:pk>', deletesuivre, name='delete-suivre'),
    path('recherche', search, name='search'),
    path('profil/<int:pk>', ProfilDetailView.as_view(), name='profil'),
    path('cours_suivis/<int:pk>', CoursSuivisView.as_view(), name='cours_suivis'),
    path('delete_cours_suivis/delete/<int:pk>', deleteCoursSuivis, name='delete_cours_suivis'),
    path('reglage', reglageCompte, name='reglage-compte'),
    path('contact', contact_login, name='contact-login'),
    path('nos_formations', formation, name='formation'),
]
