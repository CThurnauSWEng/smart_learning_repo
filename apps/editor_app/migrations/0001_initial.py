# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-02-19 05:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects_created', to='user_app.User')),
                ('editors', models.ManyToManyField(related_name='subjects_editing', to='user_app.User')),
                ('learners', models.ManyToManyField(related_name='subjects_studying', to='user_app.User')),
            ],
        ),
    ]
