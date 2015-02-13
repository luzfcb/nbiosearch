# -*- coding: utf-8 -*-
"""nbiosearch - Python wrapper to NITGEN eNBSP IndexSearch API"""

__author__ = 'Fabio C. Barrionuevo da Luz'
__email__ = 'bnafta@gmail.com'
__version__ = '0.1.0'
from cffi import FFI

ffi = FFI()
ffi.cdef(
    """
    int printf(const char *format, ...);
    """
)

c = ffi.verify(
    """
    #include <stdio.h>
    """
)


if __name__ == "__main__":
    c.printf(b"Hi There!\n")