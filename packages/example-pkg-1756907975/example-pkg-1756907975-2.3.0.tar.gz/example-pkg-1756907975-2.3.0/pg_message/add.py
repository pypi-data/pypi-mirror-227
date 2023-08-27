from cffi import FFI
import os


def add():
    ffi = FFI()
    ffi.cdef("""
        int add(int a, int b);
    """)

    lib = ffi.dlopen("libffi_test.dll" if os.name == 'nt' else "libffi_test.so")
    return lib.add(1,1)
