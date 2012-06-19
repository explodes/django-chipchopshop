import inspect

from django import forms

class FormRegistry(object):
    global _handlers

    def __init__(self):
        self.product_handlers = {}

    def register(self, product_class, form_class):
        assert(issubclass(form_class, BaseVariantForm))
        self.product_handlers[product_class] = form_class

    def get_handler(self, product_class):
        classes = inspect.getmro(product_class)
        for c in classes:
            if c in self.product_handlers:
                return self.product_handlers[c]
        raise ValueError('No form class returned for %s. Make sure that your'
                         ' forms module is loaded.' % (product_class,))

class BaseVariantForm(forms.Form):
    product = None

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        variant = kwargs.pop('variant', None)
        super(BaseVariantForm, self).__init__(*args, **kwargs)
        # If we have a Variant, fill initials with data from the instance
        if variant:
            for field in variant._meta.fields:
                name = field.name
                if not self.fields.has_key(name):
                    continue
                self.fields[name].initial = getattr(variant, name)

    def clean(self):
        variant = self.get_variant()
        if variant is None:
            raise forms.ValidationError('There are no more of that kind of %s in stock' % self.product)
        return super(BaseVariantForm, self).clean()

    def get_variant(self):
        raise NotImplemented('Cannot find variant')

registry = FormRegistry()

def register(*product_klasses):
    def register_all(form_klass):
        for product_klass in product_klasses:
            registry.register(product_klass, form_klass)
        return form_klass
    return register_all
