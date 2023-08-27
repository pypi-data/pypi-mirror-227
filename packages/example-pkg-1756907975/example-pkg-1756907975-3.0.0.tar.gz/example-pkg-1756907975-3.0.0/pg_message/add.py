# test.py 文件(如果没有 ctypes，使用 pip install ctypes 安装)
import ctypes
def add():
    ll = ctypes.cdll.LoadLibrary
    lib = ll(r"D:\pycod\pythonProject1\test.so")
    print(lib.add(3, 4))
