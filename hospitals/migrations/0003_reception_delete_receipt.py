# Generated by Django 5.0.4 on 2024-04-28 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0002_patient_sickness'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Receipt',
        ),
    ]
