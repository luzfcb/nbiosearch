import json
import os
from os.path import dirname, join
import platform

#BASE_DIR = os.path.dirname(__file__)
from cffi import FFI

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

print(BASE_DIR)
ENBSP_DIR = os.path.join(BASE_DIR, 'eNBSP')
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


print(nitgen_dinamic_library)
print(nitgen_binary_library_path)
print(nitgen_headers_include_dirs)

#nitgen_headers_include_dirs.append(nitgen_binary_library_path)

nitgen_libraries = ["pthread", "NBioBSP"]

ffi = FFI()

with open(os.path.join(BASE_DIR, '_cdefs.h')) as f:
    _cdefs = f.read()

ffi.cdef(_cdefs)


try:
    C = ffi.verify("",
        modulename='_cffi_ext',
        libraries=['NBioBSP',],
        include_dirs=nitgen_headers_include_dirs,
        library_dirs=nitgen_binary_library_path,
        runtime_library_dirs=[],
    )

except Exception as e:
    raise ImportError("nbiosearch CFFI backend couldn't find nbiosearch: %s\n"
    "Please check that you have nbiosearch headers and libraries." % e)