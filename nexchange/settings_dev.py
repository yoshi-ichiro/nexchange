from nexchange.settings import *

#
# GA for staging
#
GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-83213781-1'
GOOGLE_ANALYTICS_DOMAIN = 'staging.nexchange.ru'

# playground
#
# GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-83213781-2'
# GOOGLE_ANALYTICS_DOMAIN = 'playground.nexchange.ru'

# playground
#
# GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-83213781-3'
# GOOGLE_ANALYTICS_DOMAIN = 'nexchange.ru'

# ReCaptcha
RECAPTCHA_SITEKEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

DEBUG = True

INTERNAL_IPS = ('127.0.0.1', '192.168.99.100')
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


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
}

# Lockout only for 1 mins on dev
AXES_LOGIN_FAILURE_LIMIT = 3
AXES_COOLOFF_TIME = timedelta(minutes=5)
CELERY_ALWAYS_EAGER = True
