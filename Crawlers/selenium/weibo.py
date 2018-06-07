#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'
"""a文件夹放selenium截的图，b文件夹放24张模板，c文件夹放获取模板时匹配失败的图，用的Chrome的--headless"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from PIL import Image
import os
import numpy as np
import re


# def llogin(user, passwd, file):
#     """selenium截图验证码"""
#     url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument('lang=zh_CN.UTF-8')
#     # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 无图模式
#     options = webdriver.Chrome(chrome_options=chrome_options)  # 启动浏览器
#     options.maximize_window()  # 最大化窗口
#     options.get(url)  # 打开链接
#     options.implicitly_wait(10)  # 隐式等待10S
#
#     name = options.find_element_by_id('loginName')
#     name.send_keys(user)
#     password = options.find_element_by_id('loginPassword')
#     password.send_keys(passwd)
#     password.send_keys(Keys.ENTER)
#     time.sleep(3)
#     options.get_screenshot_as_file('a\\' + file + '.png')
#     options.close()  # 关闭浏览器


def compare_imgs(input, output):  # img格式
    """比较两张图的一维矩阵"""
    data1 = np.matrix(input.getdata())
    data2 = np.matrix(output.getdata())
    if data1.size == data2.size:
        maybe = np.sum((data1 == data2)) / data1.size
        return maybe
    else:
        print('两张图大小不一致')


# def compare_self():
#     """内部比较，查看最高相似度"""
#     # inputt = Image.open(r'D:\python\pycharm\projects\wzq\method_post\b\2143.png')
#     # outputt = Image.open(r'D:\python\pycharm\projects\wzq\method_post\c\1234.png')
#     file_list = os.listdir('b')
#     file_list = ['b\\' + x for x in file_list]
#     ffile_list = os.listdir('b')
#     ffile_list = ['b\\' + x for x in ffile_list]
#     for x in file_list:
#         for y in ffile_list:
#             inputt = Image.open(x)
#             outputt = Image.open(y)
#             result = compare_imgs(inputt, outputt)
#             if 0.9991 < result < 1:  # 0.9991242884843936
#                 print(x, y, result)


# def get_img24():
#     """获取24个模板图"""
#     with open('file.txt', 'r') as rf:
#         read = rf.read().strip('' or ' ' or '\n')
#     if read:
#         file = int(read)
#     else:
#         file = 1
#     while 1:
#         result = []
#         file_list = os.listdir('b')
#         file_list = ['b\\' + x for x in file_list]
#         img_list = [Image.open(x) for x in file_list]
#
#         llogin('18216306584', 'phivew080', str(file))
#         time.sleep(2)
#         im = Image.open('a\\' + str(file) + '.png')
#         im = im.convert('L')
#         if len(img_list) >= 24:
#             break
#
#         xx = []
#         yy = []
#         px = im.load()
#         for x in range(im.size[0]):
#             for y in range(im.size[1]):
#                 if px[x, y] > 250:
#                     xx.append(x)
#                     yy.append(y)
#         ims = im.crop((min(xx) + 20, min(yy) + 110, max(xx) - 20, max(yy) - 10))
#         pxx = ims.load()
#         for x in range(ims.size[0]):
#             for y in range(ims.size[1]):
#                 pxx[x, y] = 255 if pxx[x, y] > 240 else 0
#
#         if len(img_list) < 1:
#             ims.save('b\\' + str(100 + file) + '.png')
#         else:
#             for x in img_list:
#                 maybe = compare_imgs(x, ims)  # 比较一维矩阵
#                 result.append(maybe)
#                 print(img_list.index(x), maybe)
#             if max(result) < 0.9992:  # 比较阈值设定
#                 ims.save('b\\' + str(10000 + file) + '.png')
#             else:
#                 ims.save('c\\' + str(10000 + file) + '.png')
#         file += 1
#         with open('file.txt', 'w') as wf:
#             wf.write(str(file))


def login(user, passwd):
    """登陆"""
    url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 无图模式
    options = webdriver.Chrome(chrome_options=chrome_options)  # 启动浏览器
    options.maximize_window()  # 最大化窗口
    options.get(url)  # 打开链接
    options.implicitly_wait(10)  # 隐式等待10S

    name = options.find_element_by_id('loginName')
    name.send_keys(user)
    password = options.find_element_by_id('loginPassword')
    password.send_keys(passwd)
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    options.get_screenshot_as_file('login.png')
    return options


def move(action, start, end):
    """移动小步"""
    n = 20
    t = []
    for i in range(n):
        x = (end.location['x'] - start.location['x']) / n
        y = (end.location['y'] - start.location['y']) / n
        action.move_by_offset(x, y)
        t.append(int(time.time() * 1000))
        print(start.location['x'] + x * i, start.location['y'] + y * i)
        time.sleep(1 / n)
    return t


def main():
    # get_img24()
    # compare_self()
    options = login('xxx', 'xxx')

    file_list = os.listdir('b')
    file_list = ['b\\' + x for x in file_list]
    # 获取特征图
    im = Image.open('login.png')
    im = im.convert('L')
    xx = []
    yy = []
    px = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if px[x, y] > 250:
                xx.append(x)
                yy.append(y)
    ims = im.crop((min(xx) + 20, min(yy) + 110, max(xx) - 20, max(yy) - 10))
    pxx = ims.load()
    for x in range(ims.size[0]):
        for y in range(ims.size[1]):
            pxx[x, y] = 255 if pxx[x, y] > 240 else 0

    for x in file_list:
        get24one = Image.open(x)
        # 比较两张图一维矩阵
        maybe = compare_imgs(get24one, ims)
        if maybe > 0.9992:
            num = [int(x) for x in list(str(re.findall('\d+', str(x))[0]))]

            action = ActionChains(options)
            # 4个点元素
            dots = options.find_elements_by_class_name('patt-dots')
            # 第一个点按住
            action.move_to_element_with_offset(dots[num[0] - 1], 0, 0).click_and_hold().perform()
            # 小步移动，大步无法识别
            t1 = move(action, dots[num[0] - 1], dots[num[1] - 1])
            t2 = move(action, dots[num[1] - 1], dots[num[2] - 1])
            t3 = move(action, dots[num[2] - 1], dots[num[3] - 1])
            t1.extend(t2)
            t1.extend(t3)
            action.release().perform()
    #         t = [t1[i] - t1[0] for i in range(1, len(t1))]
    #         print(t, len(t))
    time.sleep(3)
    # 获取登陆后的源码
    source = options.page_source
    print(source)
    options.close()  # 关闭浏览器


if __name__ == "__main__":
    main()
