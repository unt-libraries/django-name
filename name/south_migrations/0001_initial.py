# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Identifier_Type'
        db.create_table(u'name_identifier_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('icon_path', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('homepage', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'name', ['Identifier_Type'])

        # Adding model 'Identifier'
        db.create_table(u'name_identifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['name.Identifier_Type'])),
            ('belong_to_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['name.Name'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'name', ['Identifier'])

        # Adding model 'Note'
        db.create_table(u'name_note', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('note', self.gf('django.db.models.fields.TextField')()),
            ('note_type', self.gf('django.db.models.fields.IntegerField')()),
            ('belong_to_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['name.Name'])),
        ))
        db.send_create_signal(u'name', ['Note'])

        # Adding model 'Variant'
        db.create_table(u'name_variant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('belong_to_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['name.Name'])),
            ('variant_type', self.gf('django.db.models.fields.IntegerField')(max_length=50)),
            ('variant', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('normalized_variant', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'name', ['Variant'])

        # Adding model 'BaseTicketing'
        db.create_table(u'name_baseticketing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stub', self.gf('django.db.models.fields.BooleanField')(default=True, unique=True)),
        ))
        db.send_create_signal(u'name', ['BaseTicketing'])

        # Adding model 'Name'
        db.create_table(u'name_name', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('normalized_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('begin', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('end', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('disambiguation', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('record_status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('merged_with', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='merged_with_name', null=True, to=orm['name.Name'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal(u'name', ['Name'])

        # Adding unique constraint on 'Name', fields ['name', 'name_id']
        db.create_unique(u'name_name', ['name', 'name_id'])

        # Adding model 'Location'
        db.create_table(u'name_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('belong_to_name', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['name.Name'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
        ))
        db.send_create_signal(u'name', ['Location'])


    def backwards(self, orm):
        # Removing unique constraint on 'Name', fields ['name', 'name_id']
        db.delete_unique(u'name_name', ['name', 'name_id'])

        # Deleting model 'Identifier_Type'
        db.delete_table(u'name_identifier_type')

        # Deleting model 'Identifier'
        db.delete_table(u'name_identifier')

        # Deleting model 'Note'
        db.delete_table(u'name_note')

        # Deleting model 'Variant'
        db.delete_table(u'name_variant')

        # Deleting model 'BaseTicketing'
        db.delete_table(u'name_baseticketing')

        # Deleting model 'Name'
        db.delete_table(u'name_name')

        # Deleting model 'Location'
        db.delete_table(u'name_location')


    models = {
        u'name.baseticketing': {
            'Meta': {'object_name': 'BaseTicketing'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stub': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'unique': 'True'})
        },
        u'name.identifier': {
            'Meta': {'ordering': "['order', 'type']", 'object_name': 'Identifier'},
            'belong_to_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['name.Name']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['name.Identifier_Type']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'name.identifier_type': {
            'Meta': {'ordering': "['label']", 'object_name': 'Identifier_Type'},
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'icon_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'name.location': {
            'Meta': {'ordering': "['status']", 'object_name': 'Location'},
            'belong_to_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['name.Name']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'})
        },
        u'name.name': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'name_id'),)", 'object_name': 'Name'},
            'begin': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'disambiguation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'merged_with': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'merged_with_name'", 'null': 'True', 'to': u"orm['name.Name']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'name_type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'normalized_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'record_status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'name.note': {
            'Meta': {'object_name': 'Note'},
            'belong_to_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['name.Name']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'note_type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'name.variant': {
            'Meta': {'object_name': 'Variant'},
            'belong_to_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['name.Name']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'normalized_variant': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variant': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'variant_type': ('django.db.models.fields.IntegerField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['name']