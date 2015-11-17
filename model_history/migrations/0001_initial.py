# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created_date', models.DateTimeField(verbose_name='created date', default=django.utils.timezone.now)),
                ('user', models.CharField(verbose_name='user', max_length=255, blank=True, null=True)),
                ('model', models.CharField(max_length=255, verbose_name='model')),
                ('object', models.CharField(max_length=255, verbose_name='object')),
                ('type', models.PositiveSmallIntegerField(verbose_name='type', choices=[(0, 'Create'), (1, 'Update'), (2, 'Delete')])),
                ('field', models.CharField(max_length=255, verbose_name='field')),
                ('old_value', models.TextField(verbose_name='old value', blank=True, null=True)),
                ('new_value', models.TextField(verbose_name='new value', blank=True, null=True)),
                ('dump', models.TextField(verbose_name='object dump', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'history of models',
                'verbose_name': "model's history",
                'ordering': ['-created_date'],
            },
            bases=(models.Model,),
        ),
    ]
