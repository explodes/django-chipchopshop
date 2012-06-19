from django import forms
from chipchop.forms import BaseVariantForm, register

from . import models

class QuantityForm(BaseVariantForm):

    quantity = forms.IntegerField(min_value=0)


@register(models.Book)
class BookVariantForm(QuantityForm):

    is_used = forms.BooleanField(required=False)
    is_rare = forms.BooleanField(required=False)

    def get_variant(self):
        try:
            return self.product.variants.get(bookvariant__is_used=self.cleaned_data.get('is_used', False), bookvariant__is_rare=self.cleaned_data.get('is_rare', False))
        except models.Variant.DoesNotExist:
            return None

@register(models.BookBag)
class BookBagVariantForm(QuantityForm):

    color = forms.ChoiceField(choices=(('GREEN', 'Green'), ('RED', 'Red'),))

    def __init__(self, *args, **kwargs):
        super(BookBagVariantForm, self).__init__(*args, **kwargs)

    def get_variant(self):
        try:
            return self.product.variants.get(bookbagvariant__color=self.cleaned_data['color'])
        except models.Variant.DoesNotExist:
            return None

