import os
from glob import glob
from setuptools import setup
from distutils.dir_util import copy_tree

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

copy_tree('silverflask/static', 'static')

setup(
    name='SilverFlask',
    version='0.0.1alpha',
    url='http://github.com/wolfv/silverflask',
    license='GPLv3',
    author='Wolf Vollprecht',
    author_email='w.vollprecht@gmail.com',
    description='SilverFlaskify your life.',
    long_description=read('README.md'),
    packages=[
        'silverflask',
        'silverflask.core',
        'silverflask.models',
        'silverflask.controllers',
        'silverflask.mixins',
    ],

    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10    ',
        'SQLAlchemy>=1'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)