from cffi import FFI

def add():
    ffi = FFI()
    ffi.cdef("""
      int add(int a, int b);
    """)

    lib = ffi.dlopen("../lib/libffi_test.dll")
    print(lib.add(3, 4))

add()