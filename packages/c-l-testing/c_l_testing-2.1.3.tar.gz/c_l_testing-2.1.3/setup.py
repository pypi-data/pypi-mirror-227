# coding=utf-8
"""Python Carson Living setup script."""
from setuptools import setup

_VERSION = '2.1.3'


def readme():
    """Pipe README.rst"""
    with open('README.rst') as desc:
        return desc.read()


setup(
    name='c_l_testing',
    packages=['carson_living'],
    version=_VERSION,
    description='A Python library to communicate with'
                ' Carson Living Residences (https://www.carson.live/)',
    long_description=readme(),
    author='Martin Riedel',
    author_email='web@riedel-it.de',
    url='https://github.com/justanz/python-carson-living-testing',
    license='Apache License 2.0',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    include_package_data=True,
    install_requires=['requests', 'pyjwt'],
    test_suite='tests',
    keywords=[
        ],
    classifiers=[
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Home Automation',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
