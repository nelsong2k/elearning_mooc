from django.contrib import admin

from help.models import Helping, Files
from .models import *


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Postulant)
admin.site.register(Cours)
admin.site.register(Formation)
admin.site.register(Tutoriel)
admin.site.register(Suivre)
admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)
admin.site.register(Helping)
admin.site.register(Files)
admin.site.register(UserProfile)
admin.site.register(TutorielLike)
