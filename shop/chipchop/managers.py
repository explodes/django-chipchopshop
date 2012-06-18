from django.db import models
from django.db.models.fields.related import SingleRelatedObjectDescriptor

class SubtypedManager(models.Manager):
    def find_subclasses(self, root):
        for a in dir(root):
            attr = getattr(root, a)
            if isinstance(attr, SingleRelatedObjectDescriptor):
                child = attr.related.model
                if (issubclass(child, root) and
                    child is not root):
                    yield a
                    for s in self.find_subclasses(child):
                        yield '%s__%s' % (a, s)

class ProductManager(SubtypedManager):
    pass

class DisplayableProductManager(SubtypedManager):
    def get_query_set(self):
        return super(DisplayableProductManager, self).get_query_set().filter(displayed=True)

class ProductAbstractManager(ProductManager):
    pass

class DisplayableProductAbstractManager(DisplayableProductManager):
    pass

class VariantManager(SubtypedManager):
    pass

class VariantAbstractManager(SubtypedManager):
    pass

class OrderAbstractManager(models.Manager):
    pass

class AddressAbstractManager(models.Manager):
    pass

class CartAbstractManager(models.Manager):
    pass

class CartItemAbstractManager(models.Manager):
    pass
