#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import socket
import time

# windows上拨号重连客户端
obj = socket.socket()
obj.connect(("127.0.0.1", 8080))
ret_bytes = obj.recv(1024)
ret_str = str(ret_bytes, encoding="utf-8")
print("...接收到连接：", ret_str)

while True:
    aa = input()
    obj.sendall(bytes(aa, encoding="utf-8"))
    data = obj.recv(1024)
    data_str = str(data, encoding="utf-8")
    print(data_str)
    if data_str == 'ip change success':
        obj.sendall(b'q')
        time.sleep(1)
        obj.close()
        break
