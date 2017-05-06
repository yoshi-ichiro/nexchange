from nexchange.settings_prod import *
from nexchange import settings

DEBUG = True

ADMINS = []


# Local and staging
INTERNAL_IPS = ('127.0.0.1', '192.168.99.100', '192.168.43.146')
ALLOWED_HOSTS += ('localhost', '192.168.43.146', 'nexchange.dev')
MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INSTALLED_APPS += [
    'debug_toolbar',
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


DATABASES = {
    'default': dj_database_url.config(default='postgis://{}:{}@{}:{}/{}'
                                      .format(user, password, host, port, db))

}


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# Lockout only for 1 mins on dev
AXES_LOGIN_FAILURE_LIMIT = 10
AXES_COOLOFF_TIME = timedelta(seconds=30)
CELERY_ALWAYS_EAGER = False

# SECRET KEY TEST
SECRET_KEY = 'zsl4+4%(%=0@f*tkf0f2u%dt&v&h_-g5mw*o25i$480=3qcb2k'

# GA for staging and test
GOOGLE_ANALYTICS_PROPERTY_ID_UK = 'UA-83213781-4'
GOOGLE_ANALYTICS_PROPERTY_ID_RU = 'UA-83213781-4'

# YANDEX
YANDEX_METRICA_ID_RU = '42222484'
YANDEX_METRICA_ID_UK = '42222484'


# ReCaptcha TEST
RECAPTCHA_SITEKEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

# OKPAY TEST
OKPAY_WALLET = ''
OKPAY_API_KEY = ''

# PAYEER TEST
PAYEER_WALLET = '287402376'
PAYEER_IPN_KEY = '12345'
PAYEER_ACCOUNT = 'P39962269'
PAYEER_API_ID = '291547231'
PAYEER_API_KEY = '12345'

# API1 TEST
API1_USER = ''
API1_PASS = ''
API1_IS_TEST = False
API1_ID_C1 = 'cb970e70-7dfa-4d80-bfad-627c863c5e23'
API1_ID_C2 = '3ba17423-50d8-4f9c-88f1-ad84872dcfc4'
API1_ID_C3 = '32339baf-3854-4204-8d46-79b2d025b036'
CARDS_RESERVE_COUNT = os.getenv('CARDS_RESERVE_COUNT',
                                settings.CARDS_RESERVE_COUNT)


# ROBOKASSA TEST
ROBOKASSA_IS_TEST = 1
ROBOKASSA_LOGIN = 'nexchangeBTC'
ROBOKASSA_PASS1 = 'SBYcBnB8Oq63KK5UB7oC'
ROBOKASSA_PASS2 = 'vaXizy98NA4rOm8Mty6l'

# API2 TEST
API2_KEY = ''
API2_SECRET = ''

# PMT
CARDPMT_API_ID = 'user'
CARDPMT_API_PASS = 'name'


# Twilio TEST
TWILIO_ACCOUNT_SID = 'ACde6c35bc29e81275dee6b9e565377900'
TWILIO_AUTH_TOKEN = 'ce656e45dd35918a0e9e76b7a4cd1ec8'
TWILIO_PHONE_FROM_UK = '+15005550006'
TWILIO_PHONE_FROM_US = '+15005550002'


# Smtp
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'onit_demo'
EMAIL_HOST_PASSWORD = ''

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
            'include_html': True,
        }
    }
}
CARDPMT_TEST_MODE = False
