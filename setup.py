
#! /usr/bin/env python
import os
from setuptools import setup, find_packages

# with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
#     README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django-name",
    version="pre-release",
    packages=find_packages(),
    include_package_data=True,

    license="BSD",
    description="Name Authority App for Django.",
    # long_description=README,
    keywords="django name citation",
    author="University of North Texas Libraries",
    # cmdclass={'test': PyTest},
    url="https://github.com/unt-libraries/django-name",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application :: User Management"
    ]
)
