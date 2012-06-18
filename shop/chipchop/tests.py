from django.test import TestCase


class TestVariantAbstractPrice(TestCase):

    def test_priceoffset(self):
        from decimal import Decimal
        from shop.chipchop.models import ProductAbstract, VariantAbstract

        p = ProductAbstract()
        p.price = Decimal('100')


        v = VariantAbstract()
        v.product = p
        v.price_offset = Decimal('-1')

        assert v.price_for_variant == Decimal('99')

        v.price_offset = None

        assert v.price_for_variant == Decimal('100')


class TestCartContributors(TestCase):

    def test_cartContributor(self):
        from decimal import Decimal
        from shop.chipchop.models import CartAbstract
        from shop.chipchop.price.contributor import CartBaseContributor

        class CartTestContributor(CartBaseContributor):

            def contribute(self, cart, current_price, billing_address=None, shipping_address=None):
                current_price.add_gross(Decimal('1'))
                return current_price

        with self.settings(CHIPCHOP_CART_PRICE_CONTRIBUTORS=(CartTestContributor(), CartTestContributor(), CartTestContributor(),)):
            cart = CartAbstract()
            cart_price = cart.cart_price(billing_address=None, shipping_address=None)
            assert cart_price.gross == Decimal('3')


class TestCartItemContributors(TestCase):

    def test_cartitem_CartItemTaxContributor(self):
        from decimal import Decimal
        from shop.chipchop.models import CartItemAbstract, ProductAbstract, VariantAbstract
        from shop.chipchop.price.contributor import CartItemQuantityContributor, CartItemTaxContributor

        p = ProductAbstract()
        p.price = Decimal('10')

        v = VariantAbstract()
        v.product = p
        v.price_offset = Decimal('-1')



        tax_rate = '0.0685'

        with self.settings(CHIPCHOP_CARTITEM_PRICE_CONTRIBUTORS=(CartItemQuantityContributor(), CartItemTaxContributor(Decimal(tax_rate)))):
            item = CartItemAbstract()
            item.variant = v
            item.quantity = 2
            item.billing_address = None
            item.shipping_address = None

            item_price = item.price

            assert item_price.gross == Decimal('18')
            assert item_price.tax == Decimal('18') * Decimal(tax_rate)
            assert item_price.net == item_price.gross + item_price.tax

    def test_cartitem_CartItemStateTaxContributor(self):
        from decimal import Decimal
        from shop.chipchop.models import CartItemAbstract, ProductAbstract, VariantAbstract
        from shop.chipchop.price.contributor import CartItemQuantityContributor, CartItemStateTaxContributor

        p = ProductAbstract()
        p.price = Decimal('10')

        v = VariantAbstract()
        v.product = p
        v.price_offset = Decimal('-1')

        tax_rate = '0.0685'

        with self.settings(CHIPCHOP_CARTITEM_PRICE_CONTRIBUTORS=(CartItemQuantityContributor(), CartItemStateTaxContributor(dict(US=dict(UT=Decimal(tax_rate)))))):
            item = CartItemAbstract()
            item.variant = v
            item.quantity = 2
            class billing:
                country = 'US'
                state = 'UT'
            item.billing_address = billing()
            item.shipping_address = None

            item_price = item.price

            assert item_price.gross == Decimal('18')
            assert item_price.tax == Decimal('18') * Decimal(tax_rate)
            assert item_price.net == item_price.gross + item_price.tax


class TestPrices(TestCase):

    def test_IAddUnknown(self):
        from shop.chipchop.price import Price

        def add_unknown():
            price = Price()
            price += object()

        def add_none():
            price = Price()
            price += None

        self.assertRaises(ArithmeticError, add_unknown)
        self.assertRaises(ArithmeticError, add_none)


    def test_IAddNone(self):
        from shop.chipchop.price import Price

        price1 = Price()
        price2 = Price()

        price1 += price2

        assert price1.gross is None
        assert price1.tax is None
        assert price1.shipping is None
        assert price1.handling is None
        assert price1.other is None
        assert price1.net is None


    def test_IAddNoneToAll(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price()
        price2 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))

        price1 += price2

        assert price1.gross == Decimal('1')
        assert price1.tax == Decimal('1')
        assert price1.shipping == Decimal('1')
        assert price1.handling == Decimal('1')
        assert price1.other == Decimal('1')
        assert price1.net == Decimal('5')


    def test_IAddAllToNone(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))
        price2 = Price()

        price1 += price2

        assert price1.gross == Decimal('1')
        assert price1.tax == Decimal('1')
        assert price1.shipping == Decimal('1')
        assert price1.handling == Decimal('1')
        assert price1.other == Decimal('1')
        assert price1.net == Decimal('5')


    def test_IAddAllToAll(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))
        price2 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))

        price1 += price2

        assert price1.gross == Decimal('2')
        assert price1.tax == Decimal('2')
        assert price1.shipping == Decimal('2')
        assert price1.handling == Decimal('2')
        assert price1.other == Decimal('2')
        assert price1.net == Decimal('10')

    def test_AddUnknown(self):
        from shop.chipchop.price import Price

        def add_unknown():
            price = Price()
            price + object()

        def add_none():
            price = Price()
            price + None

        self.assertRaises(ArithmeticError, add_unknown)
        self.assertRaises(ArithmeticError, add_none)


    def test_AddNone(self):
        from shop.chipchop.price import Price

        price1 = Price()
        price2 = Price()

        price3 = price1 + price2

        assert price3.gross is None
        assert price3.tax is None
        assert price3.shipping is None
        assert price3.handling is None
        assert price3.other is None
        assert price3.net is None


    def test_AddNoneToAll(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price()
        price2 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))

        price3 = price1 + price2

        assert price3.gross == Decimal('1')
        assert price3.tax == Decimal('1')
        assert price3.shipping == Decimal('1')
        assert price3.handling == Decimal('1')
        assert price3.other == Decimal('1')
        assert price3.net == Decimal('5')


    def test_AddAllToNone(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))
        price2 = Price()

        price3 = price1 + price2

        assert price3.gross == Decimal('1')
        assert price3.tax == Decimal('1')
        assert price3.shipping == Decimal('1')
        assert price3.handling == Decimal('1')
        assert price3.other == Decimal('1')
        assert price3.net == Decimal('5')

    def test_AddAllToAll(self):
        from decimal import Decimal
        from shop.chipchop.price import Price


        price1 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))
        price2 = Price(gross=Decimal('1'), tax=Decimal('1'), shipping=Decimal('1'), handling=Decimal('1'), other=Decimal('1'))

        price3 = price1 + price2

        assert price3.gross == Decimal('2')
        assert price3.tax == Decimal('2')
        assert price3.shipping == Decimal('2')
        assert price3.handling == Decimal('2')
        assert price3.other == Decimal('2')
        assert price3.net == Decimal('10')

    def test_addGross(self):
        from decimal import Decimal
        from shop.chipchop.price import Price

        price1 = Price(gross=None)
        price2 = Price(gross=Decimal('1'))

        assert price1.add_gross(Decimal('1')) == Decimal('1')
        assert price1.gross == Decimal('1')

        assert price2.add_gross(Decimal('1')) == Decimal('2')
        assert price2.gross == Decimal('2')

        assert price2.add_gross(None) == Decimal('2')
        assert price2.gross == Decimal('2')

        def add_weirdobj():
            price2.add_gross(object())
        self.assertRaises(ValueError, add_weirdobj)

    def test_addTax(self):
        from decimal import Decimal
        from shop.chipchop.price import Price

        price1 = Price(tax=None)
        price2 = Price(tax=Decimal('1'))

        assert price1.add_tax(Decimal('1')) == Decimal('1')
        assert price1.tax == Decimal('1')

        assert price2.add_tax(Decimal('1')) == Decimal('2')
        assert price2.tax == Decimal('2')

        assert price2.add_tax(None) == Decimal('2')
        assert price2.tax == Decimal('2')

        def add_weirdobj():
            price2.add_tax(object())
        self.assertRaises(ValueError, add_weirdobj)

    def test_addShipping(self):
        from decimal import Decimal
        from shop.chipchop.price import Price

        price1 = Price(shipping=None)
        price2 = Price(shipping=Decimal('1'))

        assert price1.add_shipping(Decimal('1')) == Decimal('1')
        assert price1.shipping == Decimal('1')

        assert price2.add_shipping(Decimal('1')) == Decimal('2')
        assert price2.shipping == Decimal('2')

        assert price2.add_shipping(None) == Decimal('2')
        assert price2.shipping == Decimal('2')

        def add_weirdobj():
            price2.add_shipping(object())
        self.assertRaises(ValueError, add_weirdobj)

    def test_addHandling(self):
        from decimal import Decimal
        from shop.chipchop.price import Price

        price1 = Price(handling=None)
        price2 = Price(handling=Decimal('1'))

        assert price1.add_handling(Decimal('1')) == Decimal('1')
        assert price1.handling == Decimal('1')

        assert price2.add_handling(Decimal('1')) == Decimal('2')
        assert price2.handling == Decimal('2')

        assert price2.add_handling(None) == Decimal('2')
        assert price2.handling == Decimal('2')

        def add_weirdobj():
            price2.add_handling(object())
        self.assertRaises(ValueError, add_weirdobj)

    def test_addOther(self):
        from decimal import Decimal
        from shop.chipchop.price import Price

        price1 = Price(other=None)
        price2 = Price(other=Decimal('1'))

        assert price1.add_other(Decimal('1')) == Decimal('1')
        assert price1.other == Decimal('1')

        assert price2.add_other(Decimal('1')) == Decimal('2')
        assert price2.other == Decimal('2')

        assert price2.add_other(None) == Decimal('2')
        assert price2.other == Decimal('2')

        def add_weirdobj():
            price2.add_other(object())
        self.assertRaises(ValueError, add_weirdobj)
