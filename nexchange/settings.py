"""
Django settings for nexchange project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys
from datetime import timedelta

from django.core.urlresolvers import reverse_lazy
from corsheaders.defaults import default_headers
from django.utils.translation import ugettext_lazy as _
import dj_database_url
import logging
from decimal import Decimal

# SECRET KEY TEST
SECRET_KEY = 'zsl4+4%(%=0@f*tkf0f2u%dt&v&h_-g5mw*o25i$480=3qcb2k'

DEFAULT_FROM_EMAIL = 'support@nexchange.io'
SUPPORT_EMAIL = DEFAULT_FROM_EMAIL
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_PATH_APP = os.path.join(TEMPLATE_PATH, 'app')

STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

API1_USER = ''
API1_PASS = ''

ADMINS = [
    ('Oleg', 'oleg@nexchange.co.uk'),
    ('Sarunas', 'sarunas@nexchange.co.uk'),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('ca', _('Catalan')),
    ('zh-hans', _('Simplified Chinese')),
]


# CUSTOM SETTINGS
GATEWAY_RESOLVE_TIME = 5
TRANSACTION_IMPORT_TIME = 20

USER_SETS_WITHDRAW_ADDRESS_MEDIAN_TIME = 30
TICKER_INTERVAL = 60
PAYMENT_IMPORT_INTERVAL = 60
TICKER_CACHE_BACKEND = 'memory'

ORDER_CACHE_LIFETIME = 60
PRICE_CACHE_LIFETIME = 30
VOLUME_CACHE_LIFETIME = 600
# ONE HOUR, AS IT CONTAINS RESERVES
CURRENCY_CACHE_LIFETIME = 60
PAIR_CACHE_LIFETIME = 3600

PAYMENT_WINDOW_SAFETY_INTERVAL = timedelta(seconds=60)
PAYMENT_DEFAULT_SEEK_INTERVAL = timedelta(hours=12)
SMS_TOKEN_VALIDITY = timedelta(minutes=5)
SMS_TOKEN_CHARS = '1234567890'
REFERRAL_CODE_LENGTH = 10
REFERRAL_CODE_CHARS = 'ABCDEFGIKJKLMNOPRSTXYZ1234567890'
SMS_MESSAGE_AUTH = _('Nexchange confirmation code: {}')
UNIQUE_REFERENCE_LENGTH = 5
UNIQUE_REFERENCE_MAX_LENGTH = 16
REFERENCE_LOOKUP_ATTEMPTS = 5
SMS_TOKEN_LENGTH = 4
PAYMENT_WINDOW = 15
MAX_EXPIRED_ORDERS_LIMIT = 3
REFERRAL_FEE = 2
RECENT_ORDERS_LENGTH = 20
UNPAID_CANCEL_WINDOW_MINUTES = 45
MAX_NUMBER_CANCEL_ORDER = 42
NUMERIC_INTERNATIONAL_PREFIX = '00'
PLUS_INTERNATIONAL_PREFIX = '+'

PHONE_START_SHOW = 4
PHONE_END_SHOW = 4
PHONE_HIDE_PLACEHOLDER = '*'

REFERRER_GET_PARAMETER = 'ref'
REFERRER_HEADER_NAME = 'x-referral-token'
REFERRER_HEADER_INDEX = 'HTTP_X_REFERRAL_TOKEN'
REFERRAL_SESSION_KEY = REFERRER_GET_PARAMETER
REFERRAL_TOKEN_CHARS = REFERRAL_CODE_CHARS

ALLOWED_HOSTS = [
    'nexchange.io',
    'www.nexchange.io',
    'n.exchange',
    'www.n.exchange',
    'api.n.exchange',
]

ALLOWED_IMAGE_FILE_EXTENSIONS = ['.jpg', '.png', '.pdf']


# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'rest_framework',
    'corsheaders',
    'core',
    'ticker',
    'accounts',
    'orders',
    'referrals',
    'payments',
    'articles',
    'verification',
    'session_security',
    'axes',
    'guardian',
    'nexchange',
    'support',
    'loginurl',
    'social_django',
    'django_fsm',
    'risk_management',
    'audit',
    'oauth2_provider',
]


SITE_ID = 1

ROBOKASSA_URL = "https://auth.robokassa.ru/Merchant/Index.aspx?" \
                "isTest={0}&MerchantLogin={1}&" \
                "OutSum={2}&InvId={3}&SignatureValue={4}&Culture=ru"

OKPAY_URL = 'https://www.okpay.com/en/account/login.html?verification={1}&' \
            'reference={2}&return_url={3}'
OKPAY_API_URL = 'https://api.okpay.com/OkPayAPI?singleWsdl'

PAYEER_API_URL = 'https://payeer.com/ajax/api/api.php'
PAYEER_IPS = ['185.71.65.92', '185.71.65.189', '149.202.17.210']


SOFORT_API_URL = 'https://api.sofort.com/api/xml'
SOFORT_USER_ID = '141789'
SOFORT_PROJECT_ID = '344411'
SOFORT_API_KEY = 'some_id'

# ADV CASH
ADV_CASH_API_NAME = 'test_api'
ADV_CASH_ACCOUNT_EMAIL = 'sarunas@onit.ws'
ADV_CASH_API_PASSWORD = 'HgkL1hcUhwUdx0V0Y1HOR7'
ADV_CASH_SCI_NAME = 'Test Sci'
ADV_CASH_SCI_PASSWORD = 'TLuY2zgQoZoy1TDW23tup3'
ADV_CASH_WALLET_USD = 'U481612001049'
ADV_CASH_WALLET_EUR = 'E116938354831'
ADV_CASH_WALLET_GBP = 'G858614605772'
ADV_CASH_WALLET_RUB = 'R093095975471'
ADV_CASH_WALLETS = [ADV_CASH_WALLET_USD, ADV_CASH_WALLET_EUR,
                    ADV_CASH_WALLET_GBP, ADV_CASH_WALLET_RUB]


CARDPMT_API_URL = 'https://gateway.cardpmt.com/api.cgi'
CARDPMT_API_ID = 'user'
CARDPMT_API_PASS = 'name'

CMSPAGES = {
    'ABOUTUS': [
        ('about_us', _('About Us')),
        ('careers', _('Careers')),
        ('press', _('Press')),
        ('conference', _('Conference')),
        ('legal_privacy', _('Legal & Privacy')),
        ('security', _('Security'))],
    'RESOURCES': [
        ('faq', _('FAQ')),
        # ('blog', _('Blog')),
        ('fees', _('Fees')),
        ('support', _('Support')),
        ('affiliates', _('Affiliate Program')),
        # ('trading_guide', _('Trading Guide'))
    ]
}

REDIS_ADDR = 'redis'
REDIS_PORT = '6379'
REDIS_SCHEME = 'redis://{}:{}/{}'
REDIS_URL_BROKER = REDIS_SCHEME.format(REDIS_ADDR, REDIS_PORT, 1)
REDIS_URL_RESULT = REDIS_SCHEME.format(REDIS_ADDR, REDIS_PORT, 2)
REDIS_URL_CACHE = REDIS_SCHEME.format(REDIS_ADDR, REDIS_PORT, 3)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL_CACHE,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "nexchange"
    }
}


CELERY_BROKER_URL = REDIS_URL_BROKER
CELERY_RESULT_BACKEND = REDIS_URL_RESULT
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']


CORE_TASKS = {
    'get_all_enabled_tickers': {
        'task': 'ticker.task_summary.get_all_tickers',
        'schedule': timedelta(seconds=TICKER_INTERVAL),
    },
    'renew_cards_reserve': {
        'task': 'accounts.task_summary.renew_cards_reserve_invoke',
        'schedule': timedelta(seconds=60),
    },
}

PAYMENT_CHECKER_TASKS = {
    # 'check_okpay_payments': {
    #     'task': 'payments.task_summary.run_okpay',
    #     'schedule': timedelta(seconds=PAYMENT_IMPORT_INTERVAL),
    # },
    # 'check_payeer_payments': {
    #     'task': 'payments.task_summary.run_payeer',
    #     'schedule': timedelta(seconds=PAYMENT_IMPORT_INTERVAL),
    # },
    # 'check_sofort_payments': {
    #     'task': 'payments.task_summary.run_sofort',
    #     'schedule': timedelta(seconds=PAYMENT_IMPORT_INTERVAL),
    # },
    # 'check_adv_cash_payments': {
    #     'task': 'payments.task_summary.run_adv_cash',
    #     'schedule': timedelta(seconds=PAYMENT_IMPORT_INTERVAL),
    # },
    'check_fiat_order_deposit_periodic': {
        'task': 'payments.task_summary.check_fiat_order_deposit_periodic',
        'schedule': timedelta(seconds=PAYMENT_IMPORT_INTERVAL),
    },
}

ORDER_RELEASE_TASKS = {
    'buy_order_release_reference_periodic': {
        'task': 'orders.task_summary.buy_order_release_reference_periodic',
        'schedule': timedelta(seconds=30),
    },
    'exchange_order_release_periodic': {
        'task': 'orders.task_summary.exchange_order_release_periodic',
        'schedule': timedelta(seconds=30),
    },
    'cancel_unpaid_order_periodic': {
        'task': 'orders.task_summary.cancel_unpaid_order_periodic',
        'schedule': timedelta(minutes=5),
    }
}

TRANSACTION_CHECKER_TASKS = {
    'import_crypto_deposit_transactions': {
        'task': 'accounts.task_summary.import_transaction_deposit_crypto_invoke',  # noqa
        'schedule': timedelta(seconds=TRANSACTION_IMPORT_TIME),
    },

    # 'import_crypto_deposit_transactions_uphold_blockchain': {
    #     'task': 'accounts.task_summary.import_transaction_deposit_uphold_blockchain_invoke',  # noqa
    #     'schedule': timedelta(seconds=10),
    # },

    'checker_transactions': {
        'task': 'accounts.task_summary.update_pending_transactions_invoke',
        'schedule': timedelta(seconds=60),
    },
}

TRADING_TASKS = {
    'reserves_balance_checker_periodic': {
        'task': 'risk_management.task_summary.'
                'reserves_balance_checker_periodic',
        'schedule': timedelta(seconds=30),
    },
    'log_current_assets': {
        'task': 'risk_management.task_summary.log_current_assets',
        'schedule': timedelta(seconds=600),
    },
    'calculate_pnls': {
        'task': 'risk_management.task_summary.calculate_pnls',
        'schedule': timedelta(hours=24),
    },
}

AUDIT_TASKS = {
    'audit_transactions': {
        'task': 'audit.task_summary.'
                'check_suspicious_transactions_all_currencies_invoke',
        'schedule': timedelta(hours=24),
    },
}

CELERY_BEAT_SCHEDULE = {}

CELERY_BEAT_SCHEDULE.update(CORE_TASKS)
# Disabled while we do not support Fiat
CELERY_BEAT_SCHEDULE.update(PAYMENT_CHECKER_TASKS)
CELERY_BEAT_SCHEDULE.update(TRANSACTION_CHECKER_TASKS)
CELERY_BEAT_SCHEDULE.update(ORDER_RELEASE_TASKS)
CELERY_BEAT_SCHEDULE.update(TRADING_TASKS)
CELERY_BEAT_SCHEDULE.update(AUDIT_TASKS)

TASKS_TIME_LIMIT = 30
TRANSACTION_IMPORT_TIME_LIMIT = TRANSACTION_IMPORT_TIME - 1
RETRY_RELEASE_TIME = 600
RETRY_RELEASE_MAX_RETRIES = 3
CARD_CHECK_TIME = 150
RETRY_CARD_CHECK_MAX_RETRIES = 5
THIRD_PARTY_TRADE_TIME = 10


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'referrals.middleware.ReferralMiddleWare',
    'core.middleware.TimezoneMiddleware',
    'core.middleware.LastSeenMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'nexchange.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH, TEMPLATE_PATH_APP],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'core.context_processors.google_analytics',
                'core.context_processors.country_code',
                'core.context_processors.sms_token_length',
                'core.context_processors.recent_orders_length',
                'articles.context_processors.cms',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # 'django.core.context_processors.request'
            ],
        },
    },
]


WSGI_APPLICATION = 'nexchange.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
# defined by env specific configuration
user = os.getenv('POSTGIS_ENV_POSTGRES_USER', 'postgres')
password = os.getenv('POSTGIS_ENV_POSTGRES_PASSWORD', '')
host = os.getenv('POSTGIS_PORT_5432_TCP_ADDR', '')
port = os.getenv('POSTGIS_PORT_5432_TCP_PORT', '')
db = os.getenv('POSTGIS_ENV_POSTGRES_DB', 'nexchange')

DATABASES = {
    'default': dj_database_url.config(default='postgis://{}:{}@{}:{}/{}'
                                      .format(user, password, host, port, db))

}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.'
        'password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        'password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        'password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        'password_validation.NumericPasswordValidator',
    },
]

AUTH_PROFILE_MODULE = 'core.Profile'

# SOCIAL Login

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
    'loginurl.backends.LoginUrlBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = (
    STATIC_PATH,
)

# General
WALLET_TIMEOUT = 999
WALLET_BACKUP_PATH = '/wallet_backup'

API1_IS_TEST = True
API1_ID_C1 = 'a1a88f60-7473-47e4-9b78-987daf198a5d'
API1_ID_C2 = '12345'
API1_ID_C3 = '54321'
API1_ID_C4 = '543216'
API1_COINS = []
API1_PAT = 'None'
CARDS_RESERVE_COUNT = 20
# this is used if there is no reserve on user.create()
EMERGENCY_CARDS_RESERVE_COUNT = 1

# API3 TEST
API3_KEY = ''
API3_SECRET = ''
API3_PUBLIC_KEY_C1 = ''

# API4 TEST
API4_KEY = ''
API4_SECRET = ''

# API5
API5_KEY = ''
API5_SECRET = ''

# RPC
RPC_IMPORT_TRANSACTIONS_COUNT = int(os.getenv('RPC_IMPORT_TRANSACTION_COUNT',
                                              10))
RPC_IMPORT_BLOCK_COUNT = int(os.getenv('RPC_IMPORT_BLOCK_COUNT', 10))
RPC_GAS_LIMIT_ETH = int(os.getenv('RPC_GAS_LIMIT_ETH', 30000))
RPC_GAS_LIMIT_TOKEN = int(os.getenv('RPC_GAS_LIMIT_TOKEN', 70000))
RPC_GAS_PRICE = int(os.getenv('RPC_GAS_PRICE', 50 * (10 ** 9)))
RPC2_PUBLIC_KEY_C1 = '123'
RPC3_PUBLIC_KEY_C1 = '456'
# RPC
DEFAULT_RPC_USER = ''
DEFAULT_RPC_PASS = ''
DEFAULT_RPC_HOST = ''


KRAKEN_PRIVATE_URL_API = "https://api.kraken.com/0/private/%s"
TWILIO_PHONE_FROM_UK = '+447481341915'
TWILIO_PHONE_FROM_US = '+16464612858'

LOGIN_REDIRECT_URL = reverse_lazy('orders.add_order')

LOCALBTC_PAIRS = ['BTCUSD']

GRAPH_HOUR_RANGES = [
    {'val': 0.1, 'name': 'Live'},
    {'val': 1, 'name': '1 Hour'},
    {'val': 4, 'name': '4 Hours'},
    {'val': 6, 'name': '6 Hours'},
    {'val': 8, 'name': '8 Hours'},
    {'val': 12, 'name': '12 Hours'},
    {'val': 16, 'name': '16 Hours'},
    {'val': 24, 'name': '1 Day'},
    {'val': 24 * 7, 'name': '7 Days'},
    {'val': 24 * 31, 'name': '1 Month'},
    {'val': 24 * 31 * 3, 'name': '3 Months'},
    {'val': 24 * 31 * 6, 'name': '6 Months'},
    {'val': 24 * 365, 'name': '1 Year'}
]
DEFAULT_HOUR_RANGE = 4

# public api
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    REFERRER_HEADER_NAME,
)

ACCESS_TOKEN_EXPIRE_SECONDS = 5184000  # two months

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope',
               'groups': 'Access to your groups'}
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'nexchange.authentication.SessionAuthenticationNoCSRF',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication'
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '180/min',
        'user': '180/min'
    }
}
# 12 months
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 * 12
SESSION_COOKIE_DOMAIN = '.nexchange.io'

# Optionally isolate session from other django sub-domains
# SESSION_COOKIE_NAME = 'nexchangesessionid'

# https://docs.djangoproject.com/en/1.9/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CONTACT = {
    'twitter': 'https://twitter.com/cryptoNexchange',
    'twitter_handle': 'CryptoNexchange',
    'facebook': 'https://facebook.com/cryptoNexchange',
    'facebook_handle': 'CryptoNexchange',
    'support_number': '+442081442192',
    'support_number_us': '+16464612858'
}

# NEW security measures

SESSION_SECURITY_WARN_AFTER = 1800
SESSION_SECURITY_EXPIRE_AFTER = 1860
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SECURITY_INSECURE = True
SESSION_SECURITY_PASSIVE_URLS = ["/en/api/v1/price/latest/",
                                 "/en/api/v1/price/history/",
                                 "/en/session_security/ping/",
                                 "https://mc.yandex.ru/webvisor/39575585",
                                 "https://mc.yandex.ru/watch/39575585"]

AXES_LOGIN_FAILURE_LIMIT = 10
AXES_USERNAME_FORM_FIELD = 'username'
AXES_COOLOFF_TIME = timedelta(minutes=30)

# SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Redirect all logs to STDOUT where they will be picked `gelf` driver
# of docker compose
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
            'include_html': True,
        },
    }
}
BASIC_LOGGING_LEVEL = logging.DEBUG
CREDIT_CARD_IS_TEST = False
CARDPMT_TEST_MODE = False

# Safe Charge
SAFE_CHARGE_IMMEDIATE_METHODS = ['cc_card']
SAFE_CHARGE_ALLOWED_REQUEST_TIME_STAMP_DIFFERENCE_SECONDS = 2
SAFE_CHARGE_ALLOWED_DMN_IPS = [
    '91.220.189.12-91.220.189.16',
    '52.16.211.57',
    '52.17.110.204'
]
SAFE_CHARGE_MERCHANT_ID = ''
SAFE_CHARGE_MERCHANT_SITE_ID = ''
SAFE_CHARGE_SECRET_KEY = ''
SAFE_CHARGE_TEST = True
SAFE_CHARGE_NOTIFY_URL = 'http://207.154.223.232:8000/en/payments/safe_charge/dmn/listen'  # noqa
SAFE_CHARGE_SUCCESS_URL = 'https://nexchange.io/order/{}'
SAFE_CHARGE_ERROR_URL = SAFE_CHARGE_SUCCESS_URL
SAFE_CHARGE_PENDING_URL = SAFE_CHARGE_SUCCESS_URL
SAFE_CHARGE_BACK_URL = SAFE_CHARGE_SUCCESS_URL

# DEFAULT order values
DEFAULT_FIAT_ORDER_DEPOSIT_AMOUNT = Decimal('100')
DEFAULT_CRYPTO_ORDER_DEPOSIT_AMOUNT_MULTIPLIER = Decimal('100')
MINIMAL_RESERVE_LEVEL_MULTIPLIER = Decimal('5')
