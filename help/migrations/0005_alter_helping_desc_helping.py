# Generated by Django 4.0.5 on 2023-05-24 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_alter_files_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helping',
            name='desc_helping',
            field=models.TextField(),
        ),
    ]
