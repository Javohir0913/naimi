# Generated by Django 5.0.6 on 2024-06-20 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0004_feedbackmodel_price'),
        ('users', '0006_alter_favoritemodel_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackimagemodel',
            name='profile_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.profilemodel'),
        ),
    ]
