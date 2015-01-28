try:
    from setuptools import setup, Extension, Distribution, find_packages
except ImportError:
    from distutils.core import setup, Extension, Distribution, find_packages

import os
import platform


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ENBSP_DIR = os.path.join(BASE_DIR, 'nbiosearch', 'eNBSP')
ENBSP_SHARED_LIBS_DIR = os.path.join(ENBSP_DIR, 'binaries')

nitgen_headers_include_dirs = [os.path.join(ENBSP_DIR, 'include')]

# is_64bits = sys.maxsize > 2**32

PLATFORM_SYSTEM = platform.system()
PLATFORM_ARCHITECTURE = platform.architecture()[0]


if '64' in PLATFORM_ARCHITECTURE and 'Linux' in PLATFORM_SYSTEM:
    nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'x64')
elif '32' in PLATFORM_ARCHITECTURE and 'Linux' in PLATFORM_SYSTEM:
    nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'x32')

if '64' in PLATFORM_ARCHITECTURE and 'Windows' in PLATFORM_SYSTEM:
    nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32')
elif '32' in PLATFORM_ARCHITECTURE and 'Windows' in PLATFORM_SYSTEM:
    nitgen_binary_library_path = os.path.join(ENBSP_SHARED_LIBS_DIR, 'win32')


nitgen_headers_include_dirs.append(nitgen_binary_library_path)

# from Cython.Distutils import build_ext
#
# nitgen_include_dirs=["/usr/local/NITGEN/eNBSP/include"]
nitgen_libraries = ["pthread", "NBioBSP"]
#
swig_opts = [ '-I%s' % i for i in nitgen_headers_include_dirs ]
swig_opts.append('-includeall')
swig_opts.append('-modern')
swig_opts.append('-Wall')
#swig_opts.append('-M')


print(swig_opts)
#swg_paran = '-I%s -L%s -l%s -Xlinker -rpath %s' % (nitgen_headers_include_dirs[0], nitgen_binary_library_path, "NBioBSP", nitgen_binary_library_path)

interfaces_names = [
#    'NBioAPI_Basic.i',
#    'NBioAPI_Error.i',
#    'NBioAPI_Type.i'
#    'NBioAPI_IndexSearchType.i',
    'NBioAPI_IndexSearch.i', 
]


#ext_modules=[ Extension('%s' % interface_name , [ os.path.join(BASE_DIR, 'nbiosearch', interface_name)], swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries) for #interface_name in interfaces_names
#]

sources = [ os.path.join(BASE_DIR, 'nbiosearch', interface_name) for interface_name in interfaces_names ]

ext_modules=[
    Extension('_NBioAPI_Basic', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Basic.i')] , swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),
    Extension('_NBioAPI_Error', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Error.i')] , swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),
    Extension('_NBioAPI_Type', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_Type.i')] , swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),
    Extension('_NBioAPI_IndexSearchType', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_IndexSearchType.i')] , swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),  
    Extension('_NBioAPI_IndexSearch', [os.path.join(BASE_DIR, 'nbiosearch', 'NBioAPI_IndexSearch.i')] , swig_opts=swig_opts, include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries)
]


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

    #install_requires=['Cython'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
      ext_modules=ext_modules,
      py_modules=['nbiosearch2'],    
    # ext_modules=[
    #     Extension("nbiosearch/_bsp_search", ["nbiosearch/bsp_search.c"],
    #               include_dirs=nitgen_headers_include_dirs, libraries=nitgen_libraries),
    # ]
)
