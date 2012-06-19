from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    # Examples:
     url(r'^$', views.home, name='home'),
     url(r'^product/(?P<slug>[A-Za-z0-9_+-]+)/$', views.product, name='product'),
     url(r'^cart/$', views.cart, name='cart'),
)
