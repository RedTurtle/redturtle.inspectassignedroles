# -*- coding: utf-8 -*-
"""Installer for the redturtle.inspectassignedroles package."""

from setuptools import find_packages
from setuptools import setup


long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='redturtle.inspectassignedroles',
    version='1.3.dev0',
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='Python Plone',
    author='Luca Bellenghi',
    author_email='info@redturtle.it',
    url='https://pypi.python.org/pypi/redturtle.inspectassignedroles',
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['redturtle'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
        'plone.api',
        'setuptools',
        'ordereddict',
        'XlsxWriter'
    ],
    extras_require={},
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
