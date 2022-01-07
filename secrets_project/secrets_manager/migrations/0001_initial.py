# Generated by Django 4.0.1 on 2022-01-07 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Secret',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, unique=True, verbose_name='Identifier of the secret')),
                ('password', models.CharField(max_length=300, verbose_name='Encoded password of the secret')),
                ('extra', models.TextField(blank=True, default='', verbose_name='Additional information about the secret')),
            ],
        ),
    ]