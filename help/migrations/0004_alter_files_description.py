# Generated by Django 4.0.5 on 2023-05-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0003_alter_files_helping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='description',
            field=models.TextField(),
        ),
    ]
