import os

# 获取当前文件所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将库文件所在目录添加到 LD_LIBRARY_PATH（Linux/macOS）或 PATH（Windows）
if os.name == 'posix':
    os.environ['LD_LIBRARY_PATH'] = f"{current_dir}/../lib:{os.environ.get('LD_LIBRARY_PATH', '')}"
elif os.name == 'nt':
    os.environ['PATH'] = f"{current_dir}/../lib;{os.environ.get('PATH', '')}"

# 现在你可以继续加载你的库并调用函数
from cffi import FFI

def add():
    ffi = FFI()
    ffi.cdef("""
        int add(int a, int b);
    """)

    lib = ffi.dlopen("libffi_test.dll" if os.name == 'nt' else "libffi_test.so")
    print(lib.add(3, 4))
