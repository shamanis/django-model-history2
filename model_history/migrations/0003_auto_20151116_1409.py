# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('model_history', '0002_history_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='field',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='field'),
            preserve_default=True,
        ),
    ]
