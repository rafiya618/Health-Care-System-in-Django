# Generated by Django 5.0.4 on 2024-04-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='sickness',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
