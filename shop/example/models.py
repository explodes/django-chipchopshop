from django.contrib.auth import models as auth
from django.db import models
from chipchop import models as chipchop

from . import managers # Custom managers that inherit from chipchop managers

class Product(chipchop.ProductAbstract):

    name = models.CharField(max_length=240, null=False, blank=False) # We want everything to have a name.
    slug = models.SlugField(max_length=240, null=False, blank=False) # We want everything to have a slug.

    objects = managers.ProductManager()

    @models.permalink
    def get_absolute_url(self):
        return ('product', [], {'slug' : self.slug})

    def __str__(self):
        return '%s' % self.name

class Variant(chipchop.VariantAbstract):

    product = models.ForeignKey(Product, unique=False, db_index=True,
                                null=False, blank=False, related_name='variants')

    stock_level = models.PositiveIntegerField(default=0, null=False, blank=False) # We want our variants to have quantities

    objects = managers.VariantManager()

    def __str__(self):
        return '"%s"' % self.product

class Order(chipchop.OrderAbstract):

    objects = managers.OrderManager()

class Address(chipchop.AddressAbstract):

    street_1 = models.CharField(max_length=250, null=True, blank=True)
    street_2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    postal = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)

    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    objects = managers.AddressManager()

class Cart(chipchop.CartAbstract):

    order = models.OneToOneField(Order, db_index=True, null=True, blank=True, related_name='carts') # Required

    owner = models.ForeignKey(auth.User, db_index=True, unique=False, null=True, blank=True) # We want our carts to be tied to a user account

    objects = managers.CartManager()

    def add_variant(self, variant, quantity):
        items = self.items.all()
        for item in items:
            if item.variant_id == variant.pk:
                item.quantity += quantity
                item.save()
                break
        else:
            self.items.create(variant=variant, quantity=quantity).save()

class CartItem(chipchop.CartItemAbstract):

    variant = models.ForeignKey(Variant, db_index=True, unique=False, null=False, blank=False, related_name='+') # Required
    cart = models.ForeignKey(Cart, db_index=True, unique=False, null=False, blank=False, related_name='items') # Required
    billing_address = models.ForeignKey(Address, db_index=True, unique=False, null=True, blank=True, related_name='+') # Required
    shipping_address = models.ForeignKey(Address, db_index=True, unique=False, null=True, blank=True, related_name='+') # Required

    objects = managers.CartItemManager()

## { NOW THE FUN STUFF }

class Book(Product):

    isbn_13 = models.CharField(max_length=13, db_index=True) # We want our books to have this property

    objects = managers.BookManager()

    def __str__(self):
        return '"%s"' % self.name

class BookVariant(Variant):

    is_used = models.BooleanField(default=False) # We are selling used books
    is_rare = models.BooleanField(default=False) # We are selling rare books

    objects = managers.BookVariantManager()

    def __str__(self):
        return '%s, %s, %s' % (self.product, 'Used' if self.is_used else 'New', 'Rare' if self.is_rare else 'Common')


class BookBag(Product):

    objects = managers.BookBagManager()

class BookBagVariant(Variant):

    color = models.CharField(max_length=10, choices=(('GREEN', 'Green'), ('RED', 'Red'),), null=False, blank=False)

    objects = managers.BookBagVariantManager()

    def __str__(self):
        return '%s, %s' % (self.product, self.color)

