from . import carts, models

def cart(request):
    shopping_cart = carts.shopping_cart(request)
    shopping_cart_price = shopping_cart.price()
    shopping_cart_items = shopping_cart.items.all()
    shopping_cart_count = sum([item.quantity for item in shopping_cart_items])
    return dict(shopping_cart=shopping_cart, shopping_cart_items=shopping_cart_items, shopping_cart_price=shopping_cart_price, shopping_cart_count=shopping_cart_count)

def products(request):
    return dict(products=models.Product.objects)
