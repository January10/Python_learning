#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import requests
import bs4
import cv2 as cv
import pytesseract
from PIL import Image


def doubanLogin(name, passwd):
    # sesion保存信息
    session = requests.session()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
    resp = session.get('https://www.douban.com/accounts/login', headers=headers).content

    data = {
        'source': 'None',
        'redir': 'https://www.douban.com/people/178200898/',
        'form_email': name,
        'form_password': passwd,
        # 'captcha-solution': img_code,
        # 'captcha-id': captcha_id,
        'login': '登陆'
    }
    try:
        # 验证码的url
        img_url = bs4.BeautifulSoup(resp, 'lxml').find('img', attrs={'id': 'captcha_image'}).get('src')
        # 获取验证码url信息
        code = requests.get(img_url)
        # 将response的二进制内容写入到文件中
        f = open('douban_img_code.png', 'wb')
        f.write(code.content)
        # 关闭文件流对象
        f.close()

        # 读取图像，支持 bmp、jpg、png、tiff 等常用格式
        img = cv.imread("douban_img_code.png", 0)
        # 创建窗口并显示图像
        # 二值化
        ret, binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

        cv.namedWindow("Image")
        cv.imshow("Image", img)
        cv.waitKey(0)

        cv.namedWindow("binary")
        cv.imshow("binary", binary)
        cv.waitKey(0)

        # image = Image.open('douban_img_code.png')
        # image.show()
        # code = pytesseract.image_to_string(image)
        # print(code)
        # 手动输入验证码
        img_code = input("请手动输入验证码为: ")
        data['captcha-solution'] = img_code

        # 释放窗口
        cv.destroyAllWindows()

        captcha_id = bs4.BeautifulSoup(resp, 'lxml').find('input', attrs={'name': 'captcha-id'}).get('value')
        data['captcha-id'] = captcha_id
    except:
        pass

    response = session.post(url='https://www.douban.com/accounts/login', data=data, headers=headers)
    print(response.text)


if __name__ == "__main__":
    doubanLogin('18021408057', 'www431819910110')
