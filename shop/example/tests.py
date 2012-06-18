from django.test import TestCase

class TestInheritance(TestCase):

    def test_product_subtype(self):
        from shop.example import models

        book = models.Book()
        book.isbn_13 = '0987123456789'
        book.price = '1.00'
        book.save()

        bookvariant = models.BookVariant()
        bookvariant.item = book
        bookvariant.save()

        assert book.get_subtype_instance() == book

        assert models.Product.objects.all()[0].book == book
        assert models.Product.objects.all()[0].get_subtype_instance() == book

    def test_cart_with_products(self):
        from shop.example import models

        book = models.Book()
        book.isbn_13 = '0987123456789'
        book.price = '1.00'
        book.save()

        bookvariant = models.BookVariant()
        bookvariant.item = book
        bookvariant.save()

        cart = models.Cart()
        cart.save()

        cartitem1 = models.CartItem()
        cartitem1.variant = bookvariant
        cartitem1.quantity = 2
        cartitem1.save()

        cartitem2 = models.CartItem()
        cartitem2.variant = bookvariant
        cartitem2.quantity = 3
        cartitem2.save()

        print cart.price()

