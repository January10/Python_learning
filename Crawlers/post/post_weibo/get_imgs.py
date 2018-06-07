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

    missing_padding = 3 - len(resp_dataa.split('|')[0]) % 3

    if missing_padding:
        resp_dataa = resp_dataa + '=' * missing_padding
    img = base64.b64decode(resp_dataa)
    print(img)

    if os.path.exists('d\\num.txt'):
        with open('d\\num.txt', 'r', encoding='utf-8') as rf:
            file = int(rf.read())
    else:
        file = 1
    with open('d\\' + str(file) + '.png', 'wb') as wf:
        wf.write(img)

    data_listt = [[0, 0], [32, 0], [64, 0], [96, 0], [128, 0],
                  [0, 32], [32, 32], [64, 32], [96, 32], [128, 32],
                  [0, 64], [32, 64], [64, 64], [96, 64], [128, 64],
                  [0, 96], [32, 96], [64, 96], [96, 96], [128, 96],
                  [0, 128], [32, 128], [64, 128], [96, 128], [128, 128],
                  ]
    im1 = Image.new('RGB', (160, 160), 'white')
    im2 = Image.open('d\\' + str(file) + '.png')
    for i in range(len(data_list)):
        x = data_list[i][0]
        y = data_list[i][1]
        im2_crop = im2.crop((x, y, x + 32, y + 32))
        im1.paste(im2_crop, (data_listt[i][0], data_listt[i][1]))
    # im1.show()
    im1.save('d\\' + str(file) + '.png')

    file += 1
    with open('d\\num.txt', 'w', encoding='utf-8') as wf:
        wf.write(str(file))


def main():
    while 1:
        login('x', 'x')  # 加入自己的账号密码


if __name__ == "__main__":
    main()
