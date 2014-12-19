from setuptools import setup, find_packages, Command


# with open('README.rst') as f:
#     long_description = f.read()


class PyTest(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='django-rest-assured',
    version='0.0.11',
    description='Django REST Assured instantly test-covers your Django REST Framework based API.',
    # long_description=long_description,
    url='https://github.com/ydaniv/django-rest-assured',
    author='Yehonatan Daniv',
    author_email='maggotfish@gmail.com',
    license='BSD',
    packages=find_packages(),
    install_requires=["django>=1.6", "djangorestframework>=2.4.3"],
    zip_safe=False,
    cmdclass={'test': PyTest},
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
