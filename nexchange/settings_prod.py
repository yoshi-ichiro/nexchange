import dj_database_url

from nexchange.settings import *  # noqa: E401

DEBUG = True

ALLOWED_HOSTS += ['nexchange.co.uk', 'nexchange.ru',
                  'www.nexchange.co.uk', 'www.nexchange.ru']

DATABASES = {
    'default': dj_database_url.config(default='postgis://{}:{}@{}:{}/{}'
                                      .format(user, password, host, port, db))

}
