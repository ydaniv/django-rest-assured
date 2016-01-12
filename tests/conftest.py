from django.conf import settings


def pytest_configure():
    settings.configure(
        ROOT_URLCONF='tests.urls',

        ALLOWED_HOSTS=['testserver'],

        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_db'
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
