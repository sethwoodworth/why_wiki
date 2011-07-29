import os
# Django settings for why_wiki project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Seth Woodworth', 'seth@sethish.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'contacts.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'America/Detroit'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname(__file__) +'/static/'
MEDIA_URL = 'static/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), './site-media/')
STATIC_URL = '/s/'

ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rfec#to-*alb3k2iwf4orjmc)jt#!+k2k=h2^t#76evqmlzzu('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'why_wiki.urls'

TEMPLATE_DIRS = (
    # Wherever you go, there you are
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    # Stock apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
)
