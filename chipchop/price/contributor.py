from decimal import Decimal

## { CARTS

class CartBaseContributor(object):

    def should_contribute(self, cart, current_price, billing_address=None, shipping_address=None):
        return True

    def contribute(self, cart, current_price, billing_address=None, shipping_address=None):
        return current_price

    def calculate(self, cart, current_price, billing_address=None, shipping_address=None):
        if self.should_contribute(cart, current_price, billing_address=billing_address, shipping_address=shipping_address):
            return self.contribute(cart, current_price, billing_address=billing_address, shipping_address=shipping_address)

## { CART ITEMS

class CartItemBaseContributor(object):

    def should_contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        return True

    def contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        return current_price

    def calculate(self, cart_item, current_price, billing_address=None, shipping_address=None):
        if self.should_contribute(cart_item, current_price, billing_address=billing_address, shipping_address=shipping_address):
            return self.contribute(cart_item, current_price, billing_address=billing_address, shipping_address=shipping_address)

class CartItemQuantityContributor(CartItemBaseContributor):

    def contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        current_price.add_gross(cart_item.variant.base_price * cart_item.quantity)

class CartItemTaxContributor(CartItemBaseContributor):

    def __init__(self, tax_rate):
        if not isinstance(tax_rate, Decimal):
            raise ValueError('tax_rate must be a Decimal.')
        self.tax_rate = tax_rate

    def contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        current_price.add_tax(current_price.gross * self.tax_rate)

class CartItemStateTaxContributor(CartItemBaseContributor):

    def __init__(self, tax_rates):
        self.tax_rates = tax_rates

    def should_contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        if billing_address is not None:
            if billing_address.country in self.tax_rates:
                if billing_address.state in self.tax_rates[billing_address.country]:
                    return True
        return False

    def contribute(self, cart_item, current_price, billing_address=None, shipping_address=None):
        tax_rate = self.tax_rates[billing_address.country][billing_address.state]
        current_price.add_tax(current_price.gross * tax_rate)

