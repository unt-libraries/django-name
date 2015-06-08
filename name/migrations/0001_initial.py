# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTicketing',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('stub', models.BooleanField(default=True, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=500)),
                ('visible', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['order', 'type'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Identifier_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(help_text=b'What kind of data is this? Personal website? Twitter?', max_length=255)),
                ('icon_path', models.CharField(help_text=b'Path to icon image?', max_length=255, blank=True)),
                ('homepage', models.URLField(help_text=b'Homepage of label. Twitter.com, Facebook.com, etc', blank=True)),
            ],
            options={
                'ordering': ['label'],
                'verbose_name': 'Identifier Type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(help_text=b'\n    <strong>\n        <a target="_blank" href="http://itouchmap.com/latlong.html">\n            iTouchMap\n        </a>\n        : this service might be useful for filling in the lat/long data\n    </strong>\n    ', max_digits=13, decimal_places=10)),
                ('longitude', models.DecimalField(help_text=b'\n    <strong>\n        <a target="_blank" href="http://itouchmap.com/latlong.html">\n            iTouchMap\n        </a>\n        : this service might be useful for filling in the lat/long data\n    </strong>\n    ', max_digits=13, decimal_places=10)),
                ('status', models.IntegerField(default=0, max_length=2, choices=[(0, b'current'), (1, b'former')])),
            ],
            options={
                'ordering': ['status'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Please use the general reverse order: LAST, FIRST', max_length=255)),
                ('normalized_name', models.CharField(help_text=b'NACO normalized form of the name', max_length=255, editable=False)),
                ('name_type', models.IntegerField(max_length=1, choices=[(0, b'Personal'), (1, b'Organization'), (2, b'Event'), (3, b'Software'), (4, b'Building')])),
                ('begin', models.CharField(help_text=b'Conforms to EDTF format YYYY-MM-DD', max_length=25, blank=True)),
                ('end', models.CharField(help_text=b'Conforms to EDTF format YYYY-MM-DD', max_length=25, blank=True)),
                ('disambiguation', models.CharField(help_text=b'Clarify to whom or what this record pertains.', max_length=255, blank=True)),
                ('biography', models.TextField(help_text=b'Compatible with MARKDOWN', blank=True)),
                ('record_status', models.IntegerField(default=0, choices=[(0, b'Active'), (1, b'Deleted'), (2, b'Suppressed')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name_id', models.CharField(unique=True, max_length=10, editable=False)),
                ('merged_with', models.ForeignKey(related_name=b'merged_with_name', blank=True, to='name.Name', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(help_text=b'Enter notes about this record here')),
                ('note_type', models.IntegerField(choices=[(0, b'Biographical/Historical'), (1, b'Deletion Information'), (2, b'Nonpublic'), (3, b'Source'), (4, b'Other')])),
                ('belong_to_name', models.ForeignKey(to='name.Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variant_type', models.IntegerField(help_text=b'Choose variant type.', max_length=50, choices=[(0, b'Acronym'), (1, b'Abbreviation'), (2, b'Translation'), (3, b'Expansion'), (4, b'Other')])),
                ('variant', models.CharField(help_text=b'Fill in the other name variants, if any.', max_length=255)),
                ('normalized_variant', models.CharField(help_text=b'NACO normalized variant text', max_length=255, editable=False)),
                ('belong_to_name', models.ForeignKey(to='name.Name')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='name',
            unique_together=set([('name', 'name_id')]),
        ),
        migrations.AddField(
            model_name='location',
            name='belong_to_name',
            field=models.ForeignKey(to='name.Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='identifier',
            name='belong_to_name',
            field=models.ForeignKey(to='name.Name'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='identifier',
            name='type',
            field=models.ForeignKey(help_text=b"Catagorize this record's identifiers here", to='name.Identifier_Type'),
            preserve_default=True,
        ),
    ]
