import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
)

tests_require = [
    'zope.annotation',
    'zope.app.appsetup',
    'zope.app.publication',
    'zope.app.wsgi[test]',
    'zope.configuration',
    'zope.container',
    'zope.principalregistry',
    'zope.securitypolicy',
    'zope.site',
    'zope.testbrowser',
    'zope.testing',
    'zope.traversing',
]

setup(
    name='grokcore.viewlet',
    version='4.0',
    author='Grok Team',
    author_email='grok-dev@zope.org',
    url='https://github.com/zopefoundation/grokcore.viewlet',
    download_url='https://pypi.org/project/grokcore.viewlet',
    description='Grok-like configuration for zope viewlets',
    long_description=long_description,
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Zope :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['grokcore'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'grokcore.component >= 2.5',
        'grokcore.security >= 1.6',
        'grokcore.view >= 2.7',
        'martian >= 0.14',
        'setuptools',
        'zope.browserpage',
        'zope.component',
        'zope.contentprovider',
        'zope.interface',
        'zope.login',
        'zope.publisher',
        'zope.security',
        'zope.viewlet',
    ],
    extras_require={'test': tests_require},
)
