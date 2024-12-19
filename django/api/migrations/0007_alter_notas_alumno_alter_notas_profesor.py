# Generated by Django 5.0.6 on 2024-12-17 03:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_alumno_correo_remove_alumno_passhash_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notas',
            name='alumno',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='alumno_notas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notas',
            name='profesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profesor_notas', to=settings.AUTH_USER_MODEL),
        ),
    ]