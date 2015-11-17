# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model_history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='status',
            field=models.PositiveSmallIntegerField(verbose_name='Status', default=0, choices=[(0, 'New'), (1, 'Revert')]),
            preserve_default=True,
        ),
    ]
