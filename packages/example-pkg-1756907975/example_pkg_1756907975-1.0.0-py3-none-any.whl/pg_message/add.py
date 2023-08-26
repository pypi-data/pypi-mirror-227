from cffi import FFI

ffi = FFI()
ffi.cdef("""
  int add(int a, int b);
""")

lib = ffi.dlopen("libffi_test.dll")
print(lib.add(3, 4))