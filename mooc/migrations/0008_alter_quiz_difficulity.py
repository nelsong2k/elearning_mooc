# Generated by Django 4.0.5 on 2023-06-05 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooc', '0007_alter_quiz_difficulity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='difficulity',
            field=models.CharField(choices=[('moyen', 'Moyen'), ('difficile', 'Difficile'), ('facile', 'Facile')], max_length=9),
        ),
    ]