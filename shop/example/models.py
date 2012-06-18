from django.contrib.auth import models as auth
from django.db import models
from shop.chipchop import models as chipchop

from . import managers # Custom managers that inherit from chipchop managers

class Product(chipchop.ProductAbstract):

    name = models.CharField(max_length=240, null=False, blank=False) # We want everything to have a name.
    slug = models.SlugField(max_length=240, null=False, blank=False) # We want everything to have a slug.

    objects = managers.ProductManager()

class Variant(chipchop.VariantAbstract):

    product = models.ForeignKey(Product, unique=False, db_index=True,
                                null=False, blank=False)

    stock_level = models.PositiveIntegerField(default=0, null=False, blank=False) # We want our variants to have quantities

    objects = managers.VariantManager()

class Order(chipchop.OrderAbstract):

    objects = managers.OrderManager()

class Address(chipchop.AddressAbstract):

    objects = managers.AddressManager()

class Cart(chipchop.CartAbstract):

    order = models.OneToOneField(Order, db_index=True, null=True, blank=True, related_name='carts') # Required

    owner = models.ForeignKey(auth.User, db_index=True, unique=False, null=True, blank=True) # We want our carts to be tied to a user account

    objects = managers.CartManager()

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

class BookVariant(Variant):

    is_used = models.BooleanField(default=False) # We are selling used books
    is_rare = models.BooleanField(default=False) # We are selling rare books

    objects = managers.BookVariantManager()


class BookBag(Product):

    objects = managers.BookBagManager()

class BookBagVariant(Variant):

    item = models.ForeignKey(BookBag, unique=False, db_index=True, null=False, blank=False, related_name='variants') # Required, link back to the item this variant is a variant of.

    color = models.CharField(max_length=10, choices=(('GREEN', 'Green'), ('RED', 'Red'),), unique=True, null=False, blank=False)

    objects = managers.BookBagVariantManager()

