# Generated by Django 5.0.6 on 2024-06-20 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_feedbackimagemodel_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmodel',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
