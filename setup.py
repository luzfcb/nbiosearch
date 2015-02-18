#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import os
import platform
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import relpath
from os.path import splitext

from setuptools import find_packages
from setuptools import setup
from distutils.core import Extension


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

PLATFORM_SYSTEM = platform.system()
PLATFORM_ARCHITECTURE = platform.architecture()[0]
if 'Windows' in PLATFORM_SYSTEM:
    nitgen_include_dir = r"D:\Program Files (x86)\NITGEN eNBSP\SDK\inc"
    #nitgen_include_dir = "D:\\Program Files\\NITGEN eNBSP x64\\SDK\\Inc"
    nitgen_libraries = ["NBioBSP"]
    library_dirs = [
        "D:\\Program Files (x86)\\NITGEN eNBSP\\SDK\\lib",
        #"D:\\Program Files (x86)\\NITGEN eNBSP\\SDK\\Bin"
        #"D:\\Program Files\\NITGEN eNBSP x64\\SDK\\Lib\\x64",
        #"D:\\Program Files\\NITGEN eNBSP x64\\SDK\\Bin\\x64"
    ]

else:

    nitgen_include_dir = "/usr/local/NITGEN/eNBSP/include"
    nitgen_libraries = ["pthread", "NBioBSP"]
    library_dirs = []

    # ext_modules=[
    #     Extension("NitgenBSP/_bsp_search", ["NitgenBSP/bsp_search.c"],
    #               include_dirs=nitgen_include_dirs, libraries=nitgen_libraries),
    # ]

ext_modules = [
    Extension(
        splitext(relpath(path, 'src').replace(os.sep, '.'))[0],
        sources=[path],
        include_dirs=[dirname(path), nitgen_include_dir],
        libraries=nitgen_libraries,
        library_dirs=library_dirs
    )
    for root, _, _ in os.walk('src')
    for path in glob(join(root, '*.c'))
]

print(ext_modules)

setup(
    name='nbiosearch',
    version='0.1.0',
    license='BSD',
    description='Python wrapper to NITGEN eNBSP IndexSearch API',
    long_description='%s\n%s' % (read('README.rst'), re.sub(':obj:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))),
    author='Fabio C. Barrionuevo da Luz',
    author_email='bnafta@gmail.com',
    url='https://github.com/luzfcb/nbiosearch',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        # 'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg: 'rst': ['docutils>=0.11'],
    },
    entry_points={
        'console_scripts': [
            'nbiosearch = nbiosearch.__main__:main'
        ]
    },
    ext_modules=ext_modules
)
