# Generated by Django 4.0.5 on 2023-06-05 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooc', '0006_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='difficulity',
            field=models.CharField(choices=[('difficile', 'Difficile'), ('moyen', 'Moyen'), ('facile', 'Facile')], max_length=9),
        ),
    ]
