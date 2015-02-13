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