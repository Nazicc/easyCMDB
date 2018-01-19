#encoding: utf-8
# import os
import pathlib

# 读文件
def read_file(path):
    # cxt = ''
    # if os.path.isfile(path):
    #     with open(path, 'rb') as handler:
    #         cxt = handler.read()
    #     cxt = cxt.decode()
    # return cxt
    cwd = pathlib.Path(path)
    if cwd.is_file():
        return cwd.read_bytes().decode() 

# 写文件
def write_file(path, cxt):
    # if not isinstance(cxt, bytes):
    #     cxt = str(cxt).encode()
    # with open(path, 'wb') as handler:
    #     handler.write(cxt)
    # return True
    cwd = pathlib.Path(path)
    if not isinstance(cxt, bytes):
        cxt = str(cxt).encode()
    cwd.write_bytes(cxt)
    return True 