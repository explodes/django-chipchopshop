from django.conf import settings
from django.db import models
from django.dispatch import receiver

from . import managers, price

class BaseModel(models.Model):

    def __str__(self):
        return self.__class__.__name__

    class Meta:
        abstract = True

class Subtyped(BaseModel):

    subtype_attr = models.CharField(max_length=500, editable=False)

    objects = managers.SubtypedManager()

    class Meta:
        abstract = True

    def get_subtype_instance(self):
        """
        Caches and returns the final subtype instance. If refresh is set,
        the instance is taken from database, no matter if cached copy
        exists.
        """
        subtype = self
        path = self.subtype_attr.split()
        whoami = self._meta.module_name
        remaining = path[path.index(whoami) + 1:]
        for r in remaining:
            subtype = getattr(subtype, r)
        return subtype

    def store_subtype(self, klass):
        if not self.id:
            path = [self]
            parents = self._meta.parents.keys()
            while parents:
                parent = parents[0]
                path.append(parent)
                parents = parent._meta.parents.keys()
            path = [p._meta.module_name for p in reversed(path)]
            self.subtype_attr = ' '.join(path)

class Product(Subtyped):

    displayed = models.BooleanField(default=True)
    ''' Override your "subclass's" save method to update this.
    Displayed products are ones that you want to show up on your site. '''

    objects = managers.ProductManager()
    displayable = managers.DisplayableProductManager()


class ProductAbstract(Product):
    ''' 
    IMPLEMENT - Add any fields you want. (name & slug recommended)
    DO NOT SUBLCLASS  - Do not sublclass your implementation. Your product
    types will have an FK back to Product.
    '''

    price = models.DecimalField(max_digits=12, decimal_places=4)
    ''' This is the standard price for an instance of your "subclass". '''

    objects = managers.ProductAbstractManager()
    displayable = managers.DisplayableProductAbstractManager()

    class Meta:
        abstract = True

class Variant(Subtyped):

    objects = managers.VariantManager()

class VariantAbstract(Subtyped):
    '''
    IMPLEMENT - Add any fields you want. (stock_level recommended)
    '''

    price_offset = models.DecimalField(max_digits=12, decimal_places=4,
                                       null=True, blank=True)
    ''' This is the how much cheaper or more expensive this variant is than the
    original item. NULL means that there is no difference. '''

    objects = managers.VariantAbstractManager()

    @property
    def price_for_variant(self):
        ''' How much this variant costs considering the price offset. '''
        if self.price_offset is not None:
            return self.item.product.price + self.price_offset
        else:
            return self.item.product.price

    class Meta:
        abstract = True

class OrderAbstract(BaseModel):
    '''
    IMPLEMENT - Add any fields you want. (dates and purchase information
    recommended)
    '''

    objects = managers.OrderAbstractManager()

    class Meta:
        abstract = True

class AddressAbstract(BaseModel):
    ''' 
    IMPLEMENT - Add any fields you want.
    '''

    street_1 = models.CharField(max_length=250, null=True, blank=True)
    street_2 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    postal = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)

    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    objects = managers.AddressAbstractManager()

    class Meta:
        abstract = True

class CartAbstract(BaseModel):
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
        for item in self.get_subtype_instance().items.all():
            current_price += item.price()

    def price(self, billing_address=None, shipping_address=None):
        cart_price = self.cart_price(billing_address=billing_address,
                                     shipping_address=shipping_address)
        item_prices = self.item_prices()
        return cart_price + item_prices


class CartItemAbstract(BaseModel):
    '''
    IMPLEMENT - Add any fields you want.
    SUBCLASS.
    '''

    ## In subclass of your implementation
    #variant = models.ForeignKey(chipchop.models.Variant, db_index=True,
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

@receiver(models.signals.pre_save)
def _store_content_type(sender, instance, **kwargs):
    if isinstance(instance, Subtyped):
        instance.store_subtype(instance)
