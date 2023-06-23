from django.contrib.auth.models import User
from django.db import models
import random


# class Answers(models.Model):
#     question_id = models.IntegerField()
#     answer = models.CharField(max_length=200)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.answer

# class QuizTaker(models.Model):
#     utilisateur = models.CharField(max_length=200)
#     pourcentage = models.CharField(max_length=200)
#     type = models.CharField(max_length=100)
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.pourcentage


class Postulant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # GENRE = [('F', 'Feminin'), ('M', 'Masculin'), ]
    # NIVEAU = [('Dr', 'Doctorat'), ('M', 'Master'), ('L', 'Licence'),
    #           ('BTS', 'BTS'), ('BAC', 'BAC'), ]

    nom = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    # pays = models.CharField(max_length=200)
    # ville = models.CharField(max_length=200)
    # genre = models.CharField(max_length=1, choices=GENRE, )
    # date_naiss = models.DateField(blank=True, null=True)
    # niveau = models.CharField(max_length=5, choices=NIVEAU)
    confirm_pwd = models.CharField(max_length=200)
    # etablissement = models.CharField(max_length=200)
    # profession = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comfirm_pwd = models.CharField(max_length=100)


class Formation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nom_formation = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    img = models.ImageField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_formation


class Cours(models.Model):
    user_cours = models.ForeignKey(User, related_name='user_cours', on_delete=models.CASCADE, null=True, blank=True)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ManyToManyField(User, through='Suivre')
    nom_cours = models.CharField(max_length=200)
    description_cours = models.CharField(max_length=200)
    full_description = models.TextField()
    # module = models.CharField(max_length=100)
    image = models.ImageField()
    date_fin = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_cours


class Tutoriel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cours = models.ForeignKey(Cours, related_name="tutoriel", on_delete=models.CASCADE, null=True, blank=True)
    video = models.FileField()
    description = models.CharField(max_length=200)
    durer = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def is_liked_by_user(self, user):
        return self.tutoriellike_set.filter(user=user).exists()

    def likes_count(self):
        return self.tutoriellike_set.count()

    def __str__(self):
        return f"{self.video} / {self.description}"


# -------------------------------------------------------------------------------------------------------------------------------------------

class TutorielLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutoriel = models.ForeignKey(Tutoriel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tutoriel')

    def __str__(self):
        return f"{self.user.username} / {self.tutoriel.description}"


# ------------------------------------------------------------------------------------------------------------------------

class Suivre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} / {self.cours.nom_cours}"


class Quiz(models.Model):
    DIFF_CHOICES = {
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="durer du quiz en minutes")
    required_score_to_pass = models.IntegerField(help_text="required score en %")
    difficulity = models.CharField(max_length=9, choices=DIFF_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} / {self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'Quizes'


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} / {self.score}"
