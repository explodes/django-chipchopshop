from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template

from . import carts, models

def home(request):
    context = {}

    return direct_to_template(request, 'example/home.html', context)

def product(request, slug):

    product = get_object_or_404(models.Product, slug=slug)

    context = {}
    context['product'] = product

    if request.method == 'POST':
        form = product.get_variant_form(request.POST)
        if form.is_valid():
            context['success'] = True
            context['form'] = product.get_variant_form()
            carts.shopping_cart(request).add_variant(form.get_variant(), form.cleaned_data['quantity'])
            return direct_to_template(request, 'example/product.html', context)
        else:
            context['form'] = form
            return direct_to_template(request, 'example/product.html', context)
    else:
        context['form'] = product.get_variant_form()

        return direct_to_template(request, 'example/product.html', context)

def cart(request):
    context = {}

    if request.method == 'POST':
        cart = carts.shopping_cart(request)
        item = get_object_or_404(models.CartItem, pk=request.POST.get('item', None), cart=cart)
        qty = int(request.POST.get('quantity', 0))
        if qty == 0:
            item.delete()
        elif qty != item.quantity:
            item.quantity = qty
            item.save()

    return direct_to_template(request, 'example/cart.html', context)
