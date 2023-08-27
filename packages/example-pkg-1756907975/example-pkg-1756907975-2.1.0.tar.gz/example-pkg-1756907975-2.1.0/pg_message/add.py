import os
from cffi import FFI

ffi = FFI()
ffi.cdef("""
    int add(int a, int b);
""")

# 获取当前模块的绝对路径
module_dir = os.path.dirname(os.path.abspath(__file__))

# 计算库文件的路径
dll_filename = "libffi_test.dll" if os.name == 'nt' else "libffi_test.so"
dll_path = os.path.join(module_dir, "..", "lib", dll_filename)

lib = ffi.dlopen(dll_path)
print(lib.add(3, 4))
