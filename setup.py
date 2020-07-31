from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-rest-assured',
    version='0.2.3',
    description='Django REST Assured instantly test-covers your Django REST Framework based API.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ydaniv/django-rest-assured',
    author='Yehonatan Daniv',
    author_email='maggotfish@gmail.com',
    license='BSD',
    packages=find_packages(),
    install_requires=["django>=1.6", "djangorestframework>=2.4.3", "six"],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
