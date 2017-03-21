from setuptools import setup, find_packages


setup(
    name='django-rest-assured',
    version='0.2.1',
    description='Django REST Assured instantly test-covers your Django REST Framework based API.',
    url='https://github.com/ydaniv/django-rest-assured',
    author='Yehonatan Daniv',
    author_email='maggotfish@gmail.com',
    license='BSD',
    packages=find_packages(),
    install_requires=["django>=1.6", "djangorestframework>=2.4.3"],
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
