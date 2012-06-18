# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table('example_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('example', ['Order'])

        # Adding model 'Address'
        db.create_table('example_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street_1', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('street_2', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('example', ['Address'])

        # Adding model 'Cart'
        db.create_table('example_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='carts', unique=True, null=True, to=orm['example.Order'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('example', ['Cart'])

        # Adding model 'CartItem'
        db.create_table('example_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('variant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['chipchop.Variant'])),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['example.Cart'])),
            ('billing_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['example.Address'])),
            ('shipping_address', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['example.Address'])),
        ))
        db.send_create_signal('example', ['CartItem'])

        # Adding model 'Book'
        db.create_table('example_book', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['chipchop.Product'], unique=True, primary_key=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=240)),
            ('isbn_13', self.gf('django.db.models.fields.CharField')(max_length=13, db_index=True)),
        ))
        db.send_create_signal('example', ['Book'])

        # Adding model 'BookVariant'
        db.create_table('example_bookvariant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subtype_attr', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('price_offset', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=4, blank=True)),
            ('stock_level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variants', to=orm['example.Book'])),
            ('is_used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_rare', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('example', ['BookVariant'])

        # Adding model 'BookBag'
        db.create_table('example_bookbag', (
            ('product_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['chipchop.Product'], unique=True, primary_key=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=240)),
        ))
        db.send_create_signal('example', ['BookBag'])

        # Adding model 'BookBagVariant'
        db.create_table('example_bookbagvariant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subtype_attr', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('price_offset', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=4, blank=True)),
            ('stock_level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variants', to=orm['example.BookBag'])),
            ('color', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('example', ['BookBagVariant'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table('example_order')

        # Deleting model 'Address'
        db.delete_table('example_address')

        # Deleting model 'Cart'
        db.delete_table('example_cart')

        # Deleting model 'CartItem'
        db.delete_table('example_cartitem')

        # Deleting model 'Book'
        db.delete_table('example_book')

        # Deleting model 'BookVariant'
        db.delete_table('example_bookvariant')

        # Deleting model 'BookBag'
        db.delete_table('example_bookbag')

        # Deleting model 'BookBagVariant'
        db.delete_table('example_bookbagvariant')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'example.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'street_1': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'street_2': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'example.book': {
            'Meta': {'object_name': 'Book'},
            'isbn_13': ('django.db.models.fields.CharField', [], {'max_length': '13', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['chipchop.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '240'})
        },
        'example.bookbag': {
            'Meta': {'object_name': 'BookBag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'product_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['chipchop.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '240'})
        },
        'example.bookbagvariant': {
            'Meta': {'object_name': 'BookBagVariant'},
            'color': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variants'", 'to': "orm['example.BookBag']"}),
            'price_offset': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'stock_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subtype_attr': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'example.bookvariant': {
            'Meta': {'object_name': 'BookVariant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_rare': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variants'", 'to': "orm['example.Book']"}),
            'price_offset': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'stock_level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'subtype_attr': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'example.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'carts'", 'unique': 'True', 'null': 'True', 'to': "orm['example.Order']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'example.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'billing_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['example.Address']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['example.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'shipping_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['example.Address']"}),
            'variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['chipchop.Variant']"})
        },
        'example.order': {
            'Meta': {'object_name': 'Order'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['example']