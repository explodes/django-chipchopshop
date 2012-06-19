from chipchop import managers as chipchop

class ProductManager(chipchop.ProductAbstractManager):
    pass

class VariantManager(chipchop.VariantAbstractManager):
    pass

class OrderManager(chipchop.OrderAbstractManager):
    pass

class AddressManager(chipchop.AddressAbstractManager):
    pass

class CartManager(chipchop.CartAbstractManager):
    pass

class CartItemManager(chipchop.CartItemAbstractManager):
    pass

# {{ Fun stuff

class BookManager(ProductManager):
    pass

class BookVariantManager(VariantManager):
    pass

class BookBagManager(ProductManager):
    pass

class BookBagVariantManager(VariantManager):
    pass
