try:
    from setuptools import setup, Extension, Distribution, find_packages
except ImportError:
    from distutils.core import setup, Extension, Distribution, find_packages

import os
import platform


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENBSP_DIR = os.path.join(BASE_DIR, 'nbiosearch', 'eNBSP')
ENBSP_SHARED_LIBS_DIR = os.path.join(ENBSP_DIR, 'bin')

nitgen_headers_include_dirs = [os.path.join(ENBSP_DIR, 'include')]

# is_64bits = sys.maxsize > 2**32

PLATFORM_SYSTEM = platform.system()
PLATFORM_ARCHITECTURE = platform.architecture()[0]


if '64' in PLATFORM_ARCHITECTURE and 'Linux' in PLATFORM_SYSTEM:
    nitgen_headers_include_dirs.append(os.path.join(ENBSP_SHARED_LIBS_DIR, 'x64'))

elif '32' in PLATFORM_ARCHITECTURE and 'Linux' in PLATFORM_SYSTEM:
    nitgen_headers_include_dirs.append(os.path.join(ENBSP_SHARED_LIBS_DIR, 'x32'))

if '64' in PLATFORM_ARCHITECTURE and 'Windows' in PLATFORM_SYSTEM:
    nitgen_headers_include_dirs.append(os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32'))
elif '32' in PLATFORM_ARCHITECTURE and 'Windows' in PLATFORM_SYSTEM:
    nitgen_headers_include_dirs.append(os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32'))

# from Cython.Distutils import build_ext
#
# nitgen_include_dirs=["/usr/local/NITGEN/eNBSP/include"]
nitgen_libraries = ["pthread", "NBioBSP"]
#
setup(
    name="nbiosearch",
    version="0.1.0",
    url="https://github.com/luzfcb/nbiosearch",

    author="Fabio C. Barrionuevo da Luz",
    author_email="bnafta@gmail.com",
    maintainer="Fabio C. Barrionuevo da Lu",
    maintainer_email="bnafta@gmail.com",

    description="Python wrapper to NITGEN eNBSP IndexSearch API",
    long_description=open('README.rst').read(),

    packages=find_packages(),

    install_requires=['Cython'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    # ext_modules=[
    #     Extension("nbiosearch/_bsp_search", ["nbiosearch/bsp_search.c"],
    #               include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),
    # ]
)
