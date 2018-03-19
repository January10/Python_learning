#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import socket
from urllib import request
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# windows上拨号重连服务端(重启华为无线路由)
class Server(object):
    @staticmethod
    def auto_start():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 8080))
        s.listen(5)  # 等待监听
        print('Waiting for connection...')
        conn, address = s.accept()  # 获得连接与客户端ip
        print("connect from：", address)
        conn.sendall(b'connecting')
        if conn:
            data_bytes = conn.recv(1024)  # 接收数据
            data_str = str(data_bytes, encoding="utf-8")

            if data_str == 'c':
                print(address, 'start change ip')
                # while 1:
                # os.system('rasdial /dis')  # 断开拨号
                # os.system('rasdial net_home xxx x')  # 拨号更换自己的账号密码

                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
                driver = webdriver.Chrome(chrome_options=chrome_options)
                driver.maximize_window()
                driver.get('http://192.168.8.1/html/home.html')
                driver.find_element_by_xpath('//*[@id="settings"]/span').click()
                driver.find_element_by_xpath('//*[@id="username"]').send_keys('admin')
                driver.find_element_by_xpath('//*[@id="password"]').send_keys('admin' + Keys.RETURN)  # 更换自己的账号密码
                time.sleep(1)
                driver.get('http://192.168.8.1/html/reboot.html')
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="reboot_apply_button"]').click()
                driver.find_element_by_xpath('//*[@id="pop_confirm"]').click()
                time.sleep(10)
                while 1:
                    try:
                        response = request.urlopen('https://www.baidu.com/', timeout=10)
                        if response.status == 200:
                            print(response.status)
                            driver.close()  # 关闭浏览器
                            os.system('taskkill /f /t /im chromedriver.exe')
                            conn.sendall(b'ip change success')
                            break
                    except:
                        pass
            elif data_str == 'q':
                conn.close()
                s.close()
                print('close collecting')
            else:
                print(address, 'Input', data_str)
                conn.sendall(b'Not Useful Input')


ss = Server()
ss.auto_start()
