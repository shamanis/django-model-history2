import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-model-history2',
    version='0.9.3',
    description='Utility to track changes in object models',
    long_description=long_description,
    license='MIT',
    url='https://github.com/shamanis/django-model-history2',
    author='Petr Bondarenko',
    author_email='mdma.zone@gmail.com',
    packages=find_packages(),
    keywords='models history revert objects',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)