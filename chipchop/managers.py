from django.db import models
from polymorphic import PolymorphicManager

class ProductAbstractManager(PolymorphicManager):
    pass

class VariantAbstractManager(PolymorphicManager):
    pass

class OrderAbstractManager(models.Manager):
    pass

class AddressAbstractManager(models.Manager):
    pass

class CartAbstractManager(models.Manager):
    pass

class CartItemAbstractManager(models.Manager):
    pass
