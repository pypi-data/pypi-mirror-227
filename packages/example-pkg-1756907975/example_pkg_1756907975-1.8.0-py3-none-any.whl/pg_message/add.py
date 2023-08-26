from cffi import FFI

import os, sys

print(os.getcwd())  # 工作路径，文件所在目录

def add():
    ffi = FFI()
    ffi.cdef("""
      int add(int a, int b);
    """)

    lib = ffi.dlopen("../lib/libffi_test.dll")
    print(lib.add(3, 4))

add()