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
    'WebTest < 1.4', # Needed to keep WebOb below 1.2
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
    "sqlalchemy-migrate",
    "repoze.what >= 1.0.8",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.what-pylons >= 1.0",
    "repoze.who==1.0.19",
    "tgext.admin >= 0.3.11",
    "repoze.what-quickstart",
    "repoze.what.plugins.sql>=1.0.1",
    "tw2.core>=2.1.1",
    "tw2.forms",
    "WebOb",
    "tgext.mobilemiddleware >= 0.4",
    "errorcats>=1.0.2",
    "pygal",
]
if os.environ.get('OPENSHIFT_REPO_DIR'):
    install_requires.append("mysql-python")

if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib', 'pysqlite'])
    install_requires.extend(['hashlib', 'pysqlite'])

setup(
    name='remysmoke',
    version='0.1',
    description='',
    author='',
    author_email='',
    #url='',
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
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

    entry_points="""
    [paste.app_factory]
    main = remysmoke.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    dependency_links=[
        "http://tg.gy/current",
        ],
    zip_safe=False
)
