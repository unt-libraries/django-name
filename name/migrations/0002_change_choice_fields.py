# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('name', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'current'), (1, b'former')]),
        ),
        migrations.AlterField(
            model_name='name',
            name='name_type',
            field=models.IntegerField(choices=[(0, b'Personal'), (1, b'Organization'), (2, b'Event'), (3, b'Software'), (4, b'Building')]),
        ),
        migrations.AlterField(
            model_name='variant',
            name='variant_type',
            field=models.IntegerField(help_text=b'Choose variant type.', choices=[(0, b'Acronym'), (1, b'Abbreviation'), (2, b'Translation'), (3, b'Expansion'), (4, b'Other')]),
        ),
    ]
