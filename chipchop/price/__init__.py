from decimal import Decimal

def add_decimal(prop):
    def decorator(func):
        def wrapper(self, add_me):
            if add_me is not None:
                if not isinstance(add_me, Decimal):
                    raise ValueError("Cannot add non-Decimal %s." % prop)
                current = getattr(self, prop, None)
                if current is None:
                    setattr(self, prop, add_me)
                else:
                    setattr(self, prop, current + add_me)
            return func(self, add_me)
        return wrapper
    return decorator

class Price(object):

    def __init__(self, gross=None, tax=None, shipping=None, handling=None, other=None):
        self.gross = gross
        self.tax = tax
        self.shipping = shipping
        self.handling = handling
        self.other = other

    @property
    def net(self):
        return self._add_two_decimals(self._add_two_decimals(self._add_two_decimals(self._add_two_decimals(self.gross, self.tax), self.shipping), self.handling), self.other)

    @property
    def shipping_handling(self):
        return self._add_two_decimals(self.shipping, self.handling)

    def _add_two_decimals(self, one, two):
        if two is None:
            return one
        if one is None:
            return two
        return one + two

    @add_decimal('gross')
    def add_gross(self, gross):
        return self.gross

    @add_decimal('tax')
    def add_tax(self, tax):
        return self.tax

    @add_decimal('shipping')
    def add_shipping(self, shipping):
        return self.shipping

    @add_decimal('handling')
    def add_handling(self, handling):
        return self.handling

    @add_decimal('other')
    def add_other(self, other):
        return self.other

    def __add__(self, other):
        if not isinstance(other, Price):
            raise ArithmeticError("Cannot add something that isn't a price")
        return Price(
            gross=self._add_two_decimals(self.gross, other.gross),
            tax=self._add_two_decimals(self.tax, other.tax),
            shipping=self._add_two_decimals(self.shipping, other.shipping),
            handling=self._add_two_decimals(self.handling, other.handling),
            other=self._add_two_decimals(self.other, other.other),
        )

    def __iadd__(self, other):
        if not isinstance(other, Price):
            raise ArithmeticError("Cannot add something that isn't a price")
        self.add_gross(other.gross)
        self.add_tax(other.tax)
        self.add_shipping(other.shipping)
        self.add_handling(other.handling)
        self.add_other(other.other)
        return self

    def __str__(self):
        return '%s: gross=%s net=%s tax=%s shipping=%s, handling=%s other=%s' % (self.__class__.__name__, self.gross, self.net, self.tax, self.shipping, self.handling, self.other)

    def __repr__(self):
        return '%s(gross=%r, tax=%r, shipping=%r, handling=%r, other=%r)' % (self.__class__.__name__, self.gross, self.tax, self.shipping, self.handling, self.other)

