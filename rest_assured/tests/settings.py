from django.conf import settings


settings.configure(
    AUTH_USER_MODEL='auth.User',
    ROOT_URLCONF='rest_assured.tests.urls',
    ALLOWED_HOSTS=['testserver'],
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.DjangoModelPermissions',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.UnicodeJSONRenderer',
        ),
        'PAGINATE_BY': 500,
        'PAGINATE_BY_PARAM': 'page_by'
    },
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'test.db'
        }
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'rest_framework',
        'rest_assured.tests',
    ])
