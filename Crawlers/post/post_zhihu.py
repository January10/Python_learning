#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import requests
import hmac
import hashlib
import time
import json
import base64
from PIL import Image
import pprint


def zhihuLogin(name, passwd):
    # sesion保存信息
    session = requests.session()

    # headers
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhihu.com",
        "User-Agent": agent,
        'Connection': 'keep-alive'
    }
    response = session.get("https://www.zhihu.com/signup", headers=headers)
    cookies = response.cookies
    # xsrf, c0 = response.cookies["_xsrf"], response.cookies["d_c0"]
    headers.update({
        "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",  # 固定值
        # "X-Xsrftoken": xsrf,
    })

    # post的各个参数
    grant_type = 'password'
    client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
    source = 'com.zhihu.web'
    # timestamp = '1525452965874'
    timestamp = str(int(time.time() * 1000))
    lang = 'en'  # 验证码中文cn/英文en,英文简单
    ref_source = 'other_'
    utm_source = ''

    # 根据js构造signature参数
    h = hmac.new(key='d1b964811afb40118a12068ff74a12f4'.encode('utf-8'), digestmod=hashlib.sha1)
    h.update((grant_type + client_id + source + timestamp).encode('utf-8'))
    signature = h.hexdigest()
    # print(signature)

    data = {
        'client_id': client_id,
        'grant_type': grant_type,
        'timestamp': timestamp,
        'source': source,
        'signature': signature,
        'username': '+86' + name,
        'password': passwd,
        # 'captcha': '{"img_size":[200,44],"input_points":[[37.5,24.1875],[132.5,28.1875]]}',
        # {"img_size":[200,44],"input_points":[[69.5,26.1875]]}
        'lang': lang,
        'ref_source': ref_source,
        'utm_source': utm_source
    }

    # 验证码的url
    session.get('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    resp = session.put('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers)
    img_captcha = json.loads(resp.text)['img_base64']
    # 将response的二进制内容写入到文件中
    with open('zhihu_img.png', 'wb') as f:
        f.write(base64.b64decode(img_captcha))

    img = Image.open('zhihu_img.png')
    img.show()

    # 手动输入验证码
    img_code = input("请手动输入验证码为: ")
    data['captcha'] = img_code
    session.post('https://www.zhihu.com/api/v3/oauth/captcha?lang=en', headers=headers, data={"input_text": img_code})
    # 释放窗口
    img.close()

    response = session.post(url='https://www.zhihu.com/api/v3/oauth/sign_in', data=data, headers=headers,
                            cookies=cookies)
    # print(response.text)
    resp = session.get(url='https://www.zhihu.com/people/january10/activities', headers=headers)
    pprint.pprint(resp.text)


if __name__ == "__main__":
    zhihuLogin('***', '***')
