# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 23:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='client',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='client',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='plate',
            old_name='client',
            new_name='user',
        ),
    ]
