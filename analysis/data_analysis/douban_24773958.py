#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import requests
import bs4
import cv2 as cv
from lxml import etree
import time
import sqlite3


def get_info(name, passwd):
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
        with open('douban_img_code.png', 'wb') as f:
            f.write(code.content)

        # 读取图像，支持 bmp、jpg、png、tiff 等常用格式
        img = cv.imread("douban_img_code.png", 0)
        # 创建窗口并显示图像
        cv.namedWindow("Image")
        cv.imshow("Image", img)
        cv.waitKey(0)
        # 手动输入验证码
        img_code = input("请手动输入验证码为: ")
        data['captcha-solution'] = img_code
        # 释放窗口
        cv.destroyAllWindows()

        captcha_id = bs4.BeautifulSoup(resp, 'lxml').find('input', attrs={'name': 'captcha-id'}).get('value')
        data['captcha-id'] = captcha_id
    except Exception as e:
        print(e)
    # 登陆
    session.post(url='https://www.douban.com/accounts/login', data=data, headers=headers)

    con = sqlite3.connect('2018_5_14.db')
    cur = con.cursor()
    try:
        cur.execute(
            'CREATE TABLE CATALOG (people VARCHAR(50) PRIMARY KEY ,vote VARCHAR(20),have_see VARCHAR(10),rate VARCHAR(10),date VARCHAR(20),comment TEXT)')
    except Exception as e:
        print(e)

    def insert_one(cur, data):
        try:
            cur.execute('INSERT INTO CATALOG VALUES (?,?,?,?,?,?)', data)
            print('insert:', data[0], data[4])
        except Exception as e:
            print(e)
            cur.execute('UPDATE CATALOG SET vote = ?,rate=? WHERE people = ?', [data[1], data[3], data[0]])
            print('update', data[0], data[4])

    with open('start.txt', 'r', encoding='utf-8')as wf:
        read = wf.read().strip(' ' or '\n')
    start = int(read)
    urls = ['https://movie.douban.com/subject/24773958/comments?start={0}&limit=20',
            'https://movie.douban.com/subject/24773958/comments?start={0}&limit=20&status=F']
    while 1:
        response = session.get(url=urls[0].format(start), headers=headers)
        # print(type(response.text))
        selector = etree.HTML(response.text)
        # infos信息
        infos = selector.xpath('//*[@id="comments"]/div')
        if len(infos) < 20:
            break
        for i in range(20):
            vote = infos[i].xpath('div[2]/h3/span[1]/span/text()')[0].strip(' ' or '\n')
            people = infos[i].xpath('div[2]/h3/span[2]/a/text()')[0].strip(' ' or '\n')
            have_see = infos[i].xpath('div[2]/h3/span[2]/span[1]/text()')[0].strip(' ' or '\n')
            rate = infos[i].xpath('div[2]/h3/span[2]/span[2]/@title')[0].strip(' ' or '\n')
            rate = '还行' if '-' in rate else rate
            date = infos[i].xpath('div[2]/h3/span[2]/span[@class="comment-time "]/@title')[0].strip(' ' or '\n')
            comment = infos[i].xpath('div[2]/p/text()')[0].strip(' ' or '\n')
            data = None
            data = [people, vote, have_see, rate, date, comment]
            insert_one(cur, data)

            # print(vote, people, have_see, rate, date, comment)
            # print(type(vote), type(people), type(have_see), type(rate), type(date), type(comment))
        #     break
        # break
        con.commit()
        with open('start.txt', 'w+', encoding='utf-8')as wf:
            wf.write(str(start))
        start += 20
        time.sleep(7)


if __name__ == "__main__":
    get_info('***', '***')
