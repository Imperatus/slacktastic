#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
]

setup_requirements = [
    'pytest-runner',
    'pygments'  # For RST rendering in IDE
]

test_requirements = [
    'pytest',
]

setup(
    author="Jurgen Buisman",
    author_email='jurgen@labela.nl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    description="Package to send Statistics over a Slack Incoming Webhook",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slacktastic',
    name='slacktastic',
    packages=['slacktastic'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/imperatus/slacktastic',
    version='0.3.0',
    zip_safe=False,
)
