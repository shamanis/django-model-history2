import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Django model history',
    version='0.9.0',
    description='Utility to track changes in object models',
    long_description=long_description,
    license='MIT',
    url='https://github.com/shamanis/django-model-history',
    author='Petr Bondarenko',
    author_email='mdma.zone@gmail.com',
    packages=find_packages(),
    keywords='models history revert objects',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: IS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)