from django.conf import settings
from django.db import models
from polymorphic import PolymorphicModel

from . import forms, managers, price

class ProductAbstract(PolymorphicModel):
    ''' 
    IMPLEMENT - Add any fields you want. (name & slug recommended)
    DO NOT SUBLCLASS  - Do not sublclass your implementation. Your product
    types will have an FK back to Product.
    '''

    price = models.DecimalField(max_digits=12, decimal_places=4)
    ''' This is the standard price for an instance of your "subclass". '''

    objects = managers.ProductAbstractManager()

    class Meta:
        abstract = True

    def get_variant_form(self, *args, **kwargs):
        kwargs['product'] = self
        return forms.registry.get_handler(self.__class__,)(*args, **kwargs)

class VariantAbstract(PolymorphicModel):
    '''
    IMPLEMENT - Add any fields you want. (stock_level recommended)
    '''

    #product = models.ForeignKey(Product, unique=False, db_index=True,
    #                            null=False, blank=False) # Required

    price_offset = models.DecimalField(max_digits=12, decimal_places=4,
                                       null=True, blank=True)
    ''' This is the how much cheaper or more expensive this variant is than the
    original item. NULL means that there is no difference. '''

    objects = managers.VariantAbstractManager()

    class Meta:
        abstract = True

    @property
    def base_price(self):
        ''' How much this variant costs considering the price offset. '''
        if self.price_offset is not None:
            return self.product.price + self.price_offset
        else:
            return self.product.price


class OrderAbstract(models.Model):
    '''
    IMPLEMENT - Add any fields you want. (dates and purchase information
    recommended)
    '''

    objects = managers.OrderAbstractManager()

    class Meta:
        abstract = True

class AddressAbstract(models.Model):
    ''' 
    IMPLEMENT - Add any fields you want.
    '''

    #street_1 = models.CharField(max_length=250, null=True, blank=True)
    #street_2 = models.CharField(max_length=250, null=True, blank=True)
    #city = models.CharField(max_length=250, null=True, blank=True)
    #state = models.CharField(max_length=250, null=True, blank=True)
    #postal = models.CharField(max_length=250, null=True, blank=True)
    #country = models.CharField(max_length=250, null=True, blank=True)

    #email_address = models.EmailField(null=True, blank=True)
    #phone_number = models.CharField(max_length=20, null=True, blank=True)

    objects = managers.AddressAbstractManager()

    class Meta:
        abstract = True

class CartAbstract(models.Model):
    '''
    IMPLEMENT - Add any fields you want (owner recommended)
              - Add a relationship (one cart to many orders) called order/carts.
    
    For stores with multiple cart types (wish-list, bookmarked items, etc)
    you will have different implementations.
    '''

    #order = models.OneToOneField(MyOrder, db_index=True, null=True, blank=True, 
    #                             related_name='carts') # Required

    objects = managers.CartAbstractManager()

    class Meta:
        abstract = True

    def cart_price(self, billing_address=None, shipping_address=None):
        contributors = settings.CHIPCHOP_CART_PRICE_CONTRIBUTORS
        current_price = price.Price()
        for contributor in contributors:
            contributor.calculate(self, current_price,
                                  billing_address=billing_address,
                                  shipping_address=shipping_address)
        return current_price

    def item_prices(self):
        current_price = price.Price()
        for item in self.items.all():
            current_price += item.price
        return current_price

    def price(self, billing_address=None, shipping_address=None):
        cart_price = self.cart_price(billing_address=billing_address,
                                     shipping_address=shipping_address)
        item_prices = self.item_prices()
        total_price = cart_price + item_prices
        return total_price

class CartItemAbstract(models.Model):
    '''
    IMPLEMENT - Add any fields you want.
    SUBCLASS.
    '''

    ## In subclass of your implementation
    #variant = models.ForeignKey(Variant, db_index=True,
    #                            unique=False, null=False, blank=False,
    #                            related_name='+') # Required
    #cart = models.ForeignKey(Cart, db_index=True, unique=False, null=False,
    #                         blank=False, related_name='items') # Required
    #billing_address = models.ForeignKey(Address, db_index=True, unique=False,
    #                                    null=True, blank=True,
    #                                    related_name='+') # Required
    #shipping_address = models.ForeignKey(Address, db_index=True, unique=False,
    #                                     null=True, blank=True,
    #                                     related_name='+') # Required

    quantity = models.PositiveIntegerField(default=1, null=False, blank=False)
    ''' How many of this item are in a cart '''

    objects = managers.CartItemAbstractManager()

    class Meta:
        abstract = True

    @property
    def price(self):
        contributors = settings.CHIPCHOP_CARTITEM_PRICE_CONTRIBUTORS
        current_price = price.Price()
        for contributor in contributors:
            contributor.calculate(self, current_price,
                                  billing_address=self.billing_address,
                                  shipping_address=self.shipping_address)
        return current_price

