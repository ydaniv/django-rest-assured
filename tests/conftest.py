from django.conf import settings
from django.core.management import call_command


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='tests.urls',

        ALLOWED_HOSTS=['testserver'],

        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test'
            }
        },

        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',

            'rest_framework',
            'tests',
        ]
    )

    try:
        from django import setup
    except ImportError:
        call_command('syncdb', interactive=False)
    else:
        setup()
        call_command('migrate')
