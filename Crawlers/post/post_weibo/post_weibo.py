#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import requests
import time
import re
import json
import base64
import os
from PIL import Image
import numpy as np
from test_js import run_js3, get_data_env
import pprint


def compare_imgs(input, output):  # img格式
    """比较两张图的一维矩阵"""
    data1 = np.matrix(input.getdata())
    data2 = np.matrix(output.getdata())
    if data1.size == data2.size:
        maybe = np.sum((data1 == data2)) / data1.size
        return maybe
    else:
        print('两张图大小不一致')


def login(username, passwd):
    url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
    headers = {
        'Host': 'passport.weibo.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    s = requests.Session()
    resp = s.get(url=url, headers=headers)
    # print(s.cookies.get_dict())  # {'SSO-DBL': '903b2dfe558d757c50a86dbd7d018964'}
    # print(str(resp.content, encoding='gb2312'))

    # 从php获取信息
    # headers['Accept'] = '*/*'
    # headers['Accept-Encoding'] = 'gzip, deflate, br'
    php = 'https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=MjIyMjIyMjI=&callback=jsonpcallback' + str(
        int(time.time() * 1000))
    headers['Host'] = 'login.sina.com.cn'
    headers[
        'Referer'] = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
    resp = s.get(url=php, headers=headers)
    resp_data = json.loads(re.findall('{.+}', resp.text)[0])
    print(resp_data)
    # print(resp.headers)

    # 图片获取
    pattern_get = 'https://captcha.weibo.com/api/pattern/get?ver=daf139fb2696a4540b298756bd06266a&source=ssologin&usrname=18021408057&line=160&side=100&radius=30&callback=pl_cb'
    headers['Host'] = 'captcha.weibo.com'
    resp = s.get(url=pattern_get, headers=headers)
    # print(resp.text)
    resp_data = json.loads(re.findall('{.+}', resp.text)[0])
    print(resp_data['id'], resp_data['path_enc'])

    resp_dataa = resp_data['path_enc'].split(',')[1]
    print(resp_dataa)
    print(resp_dataa.split('|')[0])
    print(resp_dataa.split('|')[1])

    print(base64.b64decode(resp_dataa.split('|')[1]).decode('utf-8').split('_'))
    data_list = []
    c = base64.b64decode(resp_dataa.split('|')[1]).decode('utf-8').split('_')
    h = int(c[0])
    i = int(c[1])
    j = c[2:]
    for n in range(len(j)):
        e = 160 / h
        f = 160 / i
        g1 = int(j[n]) % h * e
        g2 = int(int(j[n]) / h) * f
        data_list.append([g1, g2])
    print(data_list)

    # print(len(resp_dataa) % 3)
    # missing_padding = 3 - len(resp_dataa) % 3
    missing_padding = 3 - len(resp_dataa.split('|')[0]) % 3
    # print(missing_padding)
    if missing_padding:
        resp_dataa = resp_dataa + '=' * missing_padding
    img = base64.b64decode(resp_dataa)
    print(img)

    # if os.path.exists('num.txt'):
    #     with open('num.txt', 'r', encoding='utf-8') as rf:
    #         file = int(rf.read())
    # else:
    #     file = 1
    with open('1.png', 'wb') as wf:
        wf.write(img)
    # file += 1
    # with open('num.txt', 'w', encoding='utf-8') as wf:
    #     wf.write(str(file))
    data_listt = [[0, 0], [32, 0], [64, 0], [96, 0], [128, 0],
                  [0, 32], [32, 32], [64, 32], [96, 32], [128, 32],
                  [0, 64], [32, 64], [64, 64], [96, 64], [128, 64],
                  [0, 96], [32, 96], [64, 96], [96, 96], [128, 96],
                  [0, 128], [32, 128], [64, 128], [96, 128], [128, 128],
                  ]
    im1 = Image.new('RGB', (160, 160), 'white')
    im2 = Image.open('1.png')
    for i in range(len(data_list)):
        x = data_list[i][0]
        y = data_list[i][1]
        im2_crop = im2.crop((x, y, x + 32, y + 32))
        im1.paste(im2_crop, (data_listt[i][0], data_listt[i][1]))
    im1.show()  # 内部最高d\4213.png d\3124.png 0.9921223958333333

    file_list = os.listdir('d')
    file_list = ['d\\' + x for x in file_list]
    for x in file_list:
        get24one = Image.open(x)
        maybe = compare_imgs(get24one, im1)
        if maybe > 0.994:
            img_num = re.findall('\d+', str(x))[0]
            print(img_num)
    id = resp_data['id']
    b = img_num
    data = {
        'ver': 'daf139fb2696a4540b298756bd06266a',
        'id': id,
        'usrname': '18021408057',
        'source': 'ssologin',
        'path_enc': run_js3(b, id),
        'data_enc': get_data_env(str(img_num))
    }
    print(data['data_enc'])
    post_url = (
        'https://captcha.weibo.com/api/pattern/verify?ver={0}&id={1}&usrname={2}&source={3}&path_enc={4}&data_enc={5}'.format(
            data['ver'], data['id'], data['usrname'], data['source'], data['path_enc'], data['data_enc']))
    # headers['Accept'] = 'application/javascript, */*; q=0.8'
    resp = s.get(url=post_url, headers=headers)
    print(resp.text)

    data = {
        'username': '18021408057',  # 账号
        'password': 'xxxx',  # 加入自己的密码
        'savestate': '1',
        'r': 'http%3A%2F%2Fweibo.cn%2F',
        'ec': '0',
        'pagerefer': '',
        'entry': 'mweibo',
        'wentry': '',
        'loginfrom': '',
        'client_id': '',
        'code': '',
        'qq': '',
        'mainpageflag': '1',
        'vid': resp_data['id'],
        'hff': '',
        'hfp': '',
    }
    login_post = 'https://passport.weibo.cn/sso/login'
    headers['Host'] = 'passport.weibo.cn'
    headers['Origin'] = 'https://passport.weibo.cn'
    resp = s.post(url=login_post, data=data, headers=headers)
    print(resp.text)

    headers['Host'] = 'weibo.cn'
    resp = s.post(url='https://weibo.cn/', headers=headers)
    time.sleep(2)
    pprint.pprint(resp.text)


def main():
    login('x', 'x')


if __name__ == "__main__":
    main()
