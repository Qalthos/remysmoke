# -*- coding: utf-8 -*-
#quckstarted Options:
#
# sqlalchemy: True
# auth:       sqlalchemy
# mako:       True
#
#

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs=[
    'WebTest',
    'nose',
    'coverage',
    'wsgiref',
    'repoze.who-testutil >= 1.0.1',
]
install_requires=[
    "TurboGears2 >= 2.2",
    "Mako",
    "zope.sqlalchemy >= 0.4",
    "repoze.tm2 >= 1.0a5",
    "sqlalchemy",
    'alembic',
    "repoze.what >= 1.0.8",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.what-pylons >= 1.0",
    "repoze.who==1.0.19",
    "repoze.what-quickstart",
    "repoze.what.plugins.sql>=1.0.1",
    "tgext.mobilemiddleware >= 0.4",
    "errorcats>=1.0.2",
    "pygal",
]
if os.environ.get('OPENSHIFT_REPO_DIR'):
    install_requires.append("tg.devtools")
    install_requires.append("gevent")
    install_requires.append("mysql-python == 1.2.3") # setuptools 0.7

if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib', 'pysqlite'])
    install_requires.extend(['hashlib', 'pysqlite'])

setup(
    name='remysmoke',
    version='1.2',
    description='',
    author='',
    author_email='',
    #url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'remysmoke': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'remysmoke': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('public/**', 'ignore', None)]},
    entry_points={
        'paste.app_factory': [
            'main = remysmoke.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ],
    },
    dependency_links=[
        "http://tg.gy/230",
    ],
    zip_safe=False
)
