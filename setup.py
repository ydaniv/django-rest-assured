from setuptools import setup, find_packages


# with open('README.rst') as f:
#     long_description = f.read()


setup(
    name='django-rest-assured',
    version='0.0.5',
    description='Django REST Assured instantly test-covers your Django REST Framework based API.',
    # long_description=long_description,
    url='https://github.com/ydaniv/django-rest-assured',
    author='Yehonatan Daniv',
    author_email='maggotfish@gmail.com',
    license='BSD',
    packages=find_packages(),
    install_requires=["django >= 1.6", "djangorestframework >= 2.4.3"],
    zip_safe=False,
)
