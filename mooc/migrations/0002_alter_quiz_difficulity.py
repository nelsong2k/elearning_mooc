# Generated by Django 4.0.5 on 2023-04-13 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='difficulity',
            field=models.CharField(choices=[('facile', 'Facile'), ('moyen', 'Moyen'), ('difficile', 'Difficile')], max_length=9),
        ),
    ]
