#! /usr/bin/env python
import os
import re
from setuptools import setup, find_packages

version = ''
with open('name/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

readme = ''
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fd:
    readme = fd.read()

install_requires = [
    'python-dateutil==2.7.3',
    'markdown2==2.4.0',
    'djangorestframework==3.11.2',
    'pynaco @ git+https://github.com/unt-libraries/pynaco',
]

setup(
    name='django-name',
    version=version,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    license='BSD',
    description='Name Authority App for Django.',
    long_description=readme,
    keywords='django name citation',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    url='https://github.com/unt-libraries/django-name',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application'
    ]
)
