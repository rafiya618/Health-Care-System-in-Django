# Generated by Django 5.0.4 on 2024-04-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0003_reception_delete_receipt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drugs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('exp_date', models.DateField()),
                ('stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('mobile', models.IntegerField()),
            ],
        ),
    ]