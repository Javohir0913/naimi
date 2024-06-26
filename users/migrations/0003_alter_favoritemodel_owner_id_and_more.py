# Generated by Django 5.0.6 on 2024-06-20 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_favourite_favoritemodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritemodel',
            name='owner_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='users.profilemodel'),
        ),
        migrations.RemoveField(
            model_name='favoritemodel',
            name='profiles_id',
        ),
        migrations.AddField(
            model_name='favoritemodel',
            name='profiles_id',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='users.profilemodel'),
        ),
    ]
