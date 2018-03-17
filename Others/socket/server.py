#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import socket
import os

# windows上拨号重连服务端
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8080))
s.listen(5)  # 等待监听
print('Waiting for connection...')

while True:
    conn, address = s.accept()  # 获得连接与客户端ip
    print("...接收到连接：", address)
    conn.sendall(b'GOT IT')
    while address:
        data_bytes = conn.recv(1024)  # 接收数据
        data_str = str(data_bytes, encoding="utf-8")
        if data_str == 'c':
            print('start change ip')
            # 断开拨号
            os.system('rasdial /dis')
            # 拨号
            os.system('rasdial net_home xxxxxxxxx xxxxxxx')  # 输入拨号账号密码
            conn.sendall(b'ip change success')
        elif data_str == 'q':
            conn.close()
            break
        else:
            print(data_str, 'Not Useful Input')
            conn.sendall(b'Not Useful Input')
    s.close()
    break
print('over')
