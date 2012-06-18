# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('chipchop_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subtype_attr', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('displayed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('chipchop', ['Product'])

        # Adding model 'Variant'
        db.create_table('chipchop_variant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subtype_attr', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('chipchop', ['Variant'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table('chipchop_product')

        # Deleting model 'Variant'
        db.delete_table('chipchop_variant')


    models = {
        'chipchop.product': {
            'Meta': {'object_name': 'Product'},
            'displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtype_attr': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'chipchop.variant': {
            'Meta': {'object_name': 'Variant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtype_attr': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['chipchop']