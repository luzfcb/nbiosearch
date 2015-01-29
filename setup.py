#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, Extension, Distribution
except ImportError:
    from distutils.core import setup, Extension, Distribution

import os
import platform

from Cython.Build import cythonize


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

BASE_DIR = os.path.dirname(__file__)
ENBSP_DIR = os.path.join(BASE_DIR, 'nbiosearch', 'eNBSP')
ENBSP_SHARED_LIBS_DIR = os.path.join(ENBSP_DIR, 'binaries')

ENBSP_HEADERS_INCLUDE_DIR = os.path.join(ENBSP_DIR, 'include')

nitgen_headers_include_dirs = [ENBSP_HEADERS_INCLUDE_DIR]

PLATFORM_SYSTEM = platform.system()
PLATFORM_ARCHITECTURE = platform.architecture()[0]

nitgen_dinamic_library = []

if 'Linux' in PLATFORM_SYSTEM:
    if '64' in PLATFORM_ARCHITECTURE:
        nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'x64')
        nitgen_dinamic_library = [os.path.join(nitgen_binary_library_path, 'libNBioBSP.so')]
    elif '32' in PLATFORM_ARCHITECTURE:
        nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'x32')
        nitgen_dinamic_library = [os.path.join(nitgen_binary_library_path, 'libNBioBSP.so')]
    else:
        print('PLATFORM_ARCHITECTURE does not detected')
elif 'Windows' in PLATFORM_SYSTEM:
    if '64' in PLATFORM_ARCHITECTURE:
        nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32')
        nitgen_dinamic_library = [
            os.path.join(nitgen_binary_library_path, 'NSearch.dll'),
            os.path.join(nitgen_binary_library_path, 'NBioBSP.dll'),
        ]
    elif '32' in PLATFORM_ARCHITECTURE:
        nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32')
        nitgen_dinamic_library = [
            os.path.join(nitgen_binary_library_path, 'NSearch.dll'),
            os.path.join(nitgen_binary_library_path, 'NBioBSP.dll'),
        ]
    else:
        print('PLATFORM_ARCHITECTURE does not detected')
else:
    print('PLATFORM_SYSTEM does not detected. This library only works with Linux and Windows')

nitgen_headers_include_dirs.append(nitgen_binary_library_path)

nitgen_libraries = ["pthread", "NBioBSP"]

swig_opts = ['-I".{0}" -L".{0}"'.format(lib_path) for lib_path in nitgen_headers_include_dirs]
swig_opts.append('-includeall')
swig_opts.append('-modern')
swig_opts.append('-Wall')
swig_opts.append('-MM')




# swig_interface_names = [
# 'NBioAPI_Basic.i',
#    'NBioAPI_Error.i',
#    'NBioAPI_Type.i'
#    'NBioAPI_IndexSearchType.i',
#    'NBioAPI_IndexSearch.i',
#]

ext_modules = [
    # Extension('_NBioAPI_Basic', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Basic.i')], swig_opts=swig_opts,
    #           include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
    #           library_dirs=nitgen_headers_include_dirs,
    #           extra_link_args=nitgen_dinamic_library
    # ),
    # Extension('_NBioAPI_Error', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Error.i')], swig_opts=swig_opts,
    #           include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
    #           library_dirs=nitgen_headers_include_dirs,
    #           extra_link_args=nitgen_dinamic_library
    # ),
    # Extension('_NBioAPI_Type', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Type.i')], swig_opts=swig_opts,
    #           include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
    #           library_dirs=nitgen_headers_include_dirs,
    #           extra_link_args=nitgen_dinamic_library
    # ),
    # Extension('_NBioAPI_IndexSearchType', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_IndexSearchType.i')],
    #           swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
    #           library_dirs=nitgen_headers_include_dirs,
    #           extra_link_args=nitgen_dinamic_library
    # ),
    # Extension('_NBioAPI_IndexSearch', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_IndexSearch.i')],
    #           swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
    #           library_dirs=nitgen_headers_include_dirs,
    #           extra_link_args=nitgen_dinamic_library
    # )
]
a = os.path.join(BASE_DIR, 'nbiosearch', "*.pyd")
print(a)
setup(
    name='nbiosearch',
    version='0.1.0',
    description='Python wrapper to NITGEN eNBSP IndexSearch API',
    long_description=readme + '\n\n' + history,
    author='Fabio C. Barrionuevo da Luz',
    author_email='bnafta@gmail.com',
    url='https://github.com/luzfcb/nbiosearch',
    packages=[
        'nbiosearch',
    ],
    package_dir={'nbiosearch':
                     'nbiosearch'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='nbiosearch',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    #ext_modules=ext_modules,
    ext_modules=cythonize(os.path.join(BASE_DIR, 'nbiosearch', "*.pyx"),
               include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries,
               library_dirs=nitgen_headers_include_dirs,
               extra_link_args=nitgen_dinamic_library
    ),
    py_modules=['nbiosearch']
)
