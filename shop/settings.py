import os

rel = lambda * x: os.path.abspath(os.path.join(os.path.dirname(__file__), *x))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': rel('../database.sqlite'),
    }
}

TIME_ZONE = 'US/Mountain'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = ''
MEDIA_URL = ''

STATIC_ROOT = ''
STATIC_URL = '/static/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '=ogf*xcv23f(@j01p^&hprv7xhitj%sfixrd)+v(i*tlty&gk'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'ChipChopShop.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'south',
    'polymorphic',

    'chipchop', # Required for unit tests
    'example', # Required for example shop
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from decimal import Decimal
from chipchop.price import contributor

''' Contributors that apply to the entire cart. '''
CHIPCHOP_CART_PRICE_CONTRIBUTORS = (
)

''' Contributors that apply to individual items. '''
CHIPCHOP_CARTITEM_PRICE_CONTRIBUTORS = (
    contributor.CartItemQuantityContributor(), # Adds price * quantity to the line item gross price
    contributor.CartItemTaxContributor(Decimal('0.0685')), # Taxes each item, independent of location. Utah online sales tax, as of this time, is 6.85%
    contributor.CartItemStateTaxContributor(dict(US=dict(UT=Decimal('0.0685')))), # Tax only US-UT 6.85%

)
