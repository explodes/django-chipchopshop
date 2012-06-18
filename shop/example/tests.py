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
