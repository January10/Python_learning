#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

from wzq.scrapytools.useragents import USER_AGENT
import random
import time
from urllib import request
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import urllib
import json
import copy
import re


def first_check(func):
    """开始验证文件中已存在的ips"""

    def wrapper(self, *args, **kwargs):
        with open('poolproxy.txt', 'r', encoding='utf-8') as f:
            line = f.readline().strip('\n')
            if line:
                line0 = json.loads(line)
                lines_list = f.readlines()
                pool = ThreadPoolExecutor(max_workers=100)
                for x in lines_list:
                    x = x.strip('\n')
                    pool.submit(self.check_ip, x, spider_name='first')  # 此spider_name随意，并不需要处理
                pool.shutdown()
                with open('poolproxy.txt', 'w', encoding='utf-8') as wf:
                    wf.write(json.dumps(line0))
                    wf.write('\n')
                for line in list(self.ips_useful):
                    with open('poolproxy.txt', 'a', encoding='utf-8') as af:
                        af.write(line + '\n')
            else:
                pass
        return func(self, *args, **kwargs)

    return wrapper


class PoolProxy(object):
    def __init__(self):
        self.ips_useful = set({})  # 最后的有效ips(set)
        self.latest_time = {}  # 文件中最新有效ip的时间戳
        self.latest_useful = {}  # 队列中最新有效ip的时间戳
        self.proxy_list = []  # http类有效代理列表
        self.proxy = None  # 用来爬代理的代理
        self.file_list = []  # 文本每行组成的队列

    @first_check
    def read_file(self):
        """获取文本内容"""
        with open('poolproxy.txt', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip('\n')
            if first_line:  # 如果文件有值，深拷贝
                line = json.loads(first_line)
                self.latest_useful = line
                self.latest_time = copy.deepcopy(line)
                lines = f.readlines()
                for x in lines:
                    self.file_list.append(x.strip('\n'))
            else:  # 如果文件空，设置初始时间戳
                t = int(time.mktime(time.strptime('2018-04-03 00:00:00', "%Y-%m-%d %H:%M:%S")))
                self.latest_useful = {'xici': t, 'kuaidaili': t, 'ihuan': t, 'ip3366': t}
                self.latest_time = copy.deepcopy({'xici': t, 'kuaidaili': t, 'ihuan': t, 'ip3366': t})

    def get_response(self, start_url):
        """使用代理,根据url获取html内容"""
        headers = {'User-Agent': random.choice(USER_AGENT)}
        req = request.Request(url=start_url, headers=headers)
        while 1:
            if self.proxy:
                opener = urllib.request.build_opener(urllib.request.ProxyHandler(self.proxy))  # 使用代理
                try:
                    resp = opener.open(req, timeout=5)
                    html = etree.HTML(str(resp.read(), encoding='utf-8')) if 'ihuan' in start_url else etree.HTML(
                        resp.read())
                    return html
                except Exception as e:
                    if self.proxy_list:
                        self.proxy_list.pop()
                        self.proxy = self.proxy_list[-1] if self.proxy_list else None
                        time.sleep(1)
            else:
                try:
                    req.host = req.origin_req_host  # 重置代理host
                    resp = request.urlopen(req, timeout=5)
                    html = etree.HTML(str(resp.read(), encoding='utf-8')) if 'ihuan' in start_url else etree.HTML(
                        resp.read())
                    return html
                except Exception as e:
                    print('ERROR', start_url, e)
                    time.sleep(1)

    def get_ips_xici(self):
        """根据html提取ips"""
        start_url = 'http://www.xicidaili.com/nn/1'
        while 1:
            ips_list = []
            html = self.get_response(start_url)
            print(start_url, '当前使用的代理:', self.proxy)
            # 提取信息
            ips = html.xpath('//*[@id="ip_list"]/tr/td[2]/text()')
            ports = html.xpath('//*[@id="ip_list"]/tr/td[3]/text()')
            styles = html.xpath('//*[@id="ip_list"]/tr/td[6]/text()')
            ips_time = html.xpath('//*[@id="ip_list"]/tr/td[10]/text()')
            next_url = 'http://www.xicidaili.com' + html.xpath('//*[@id="body"]/div[2]/a[last()]/@href')[0]
            for ip, port, style, ip_time in zip(ips, ports, styles, ips_time):
                ip_time = str(int(time.mktime(time.strptime('20' + ip_time + ':00', "%Y-%m-%d %H:%M:%S"))))
                item = ','.join([ip, port, style.lower(), ip_time, '0', '0'])
                ips_list.append(item)
            sign = self.get_item(ips_list, spider_name='xici')  # 增量信号到达判断
            if sign:
                break
            time.sleep(7)
            start_url = next_url

    def get_ips_ip3366(self):
        """根据html提取ips"""
        start_url = 'http://www.ip3366.net/?stype=1&page=1'
        page = 1
        while 1:
            page += 1
            ips_list = []
            html = self.get_response(start_url)
            print(start_url, '当前使用的代理:', self.proxy)
            # 提取信息
            ips = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
            ports = html.xpath('//*[@id="list"]/table/tbody/tr/td[2]/text()')
            styles = html.xpath('//*[@id="list"]/table/tbody/tr/td[4]/text()')
            ips_time = html.xpath('//*[@id="list"]/table/tbody/tr/td[8]/text()')
            next_url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
            for ip, port, style, ip_time in zip(ips, ports, styles, ips_time):
                ip_time = re.sub(r'[/]+', r'-', ip_time)
                ip_time = str(int(time.mktime(time.strptime(ip_time, "%Y-%m-%d %H:%M:%S"))))
                item = ','.join([ip, port, style.lower(), ip_time, '0', '0'])
                ips_list.append(item)
            sign = self.get_item(ips_list, spider_name='ip3366')  # 增量信号到达判断
            if sign:
                break
            time.sleep(7)
            start_url = next_url

    def get_ips_kuaidaili(self):
        """根据html提取ips"""
        start_url = 'https://www.kuaidaili.com/free/inha/1'
        page = 1
        while 1:
            page = int(page) + 1
            ips_list = []
            html = self.get_response(start_url)
            print(start_url, '当前使用的代理:', self.proxy)
            # 提取信息
            ips = html.xpath('//*[@id="list"]/table/tbody/tr/td[1]/text()')
            ports = html.xpath('//*[@id="list"]/table/tbody/tr/td[2]/text()')
            styles = html.xpath('//*[@id="list"]/table/tbody/tr/td[4]/text()')
            ips_time = html.xpath('//*[@id="list"]/table/tbody/tr/td[7]/text()')
            next_url = 'https://www.kuaidaili.com/free/inha/' + str(page)
            for ip, port, style, ip_time in zip(ips, ports, styles, ips_time):
                ip_time = str(int(time.mktime(time.strptime(ip_time, "%Y-%m-%d %H:%M:%S"))))
                item = ','.join([ip, port, style.lower(), ip_time, '0', '0'])
                ips_list.append(item)
            sign = self.get_item(ips_list, spider_name='kuaidaili')  # 增量信号到达判断
            if sign:
                break
            time.sleep(7)
            start_url = next_url

    def get_ips_ihuan(self):
        """根据html提取ips"""
        start_url = 'https://ip.ihuan.me/?page=1&anonymity=2'  # 注意此网站首页自动刷新
        k = 0
        while 1:
            ips_list = []
            html = self.get_response(start_url)
            print(start_url, '当前使用的代理:', self.proxy)
            # 提取信息
            ips = html.xpath('//*[@class="table table-hover table-bordered"]/tbody/tr/td[1]/a/text()')
            ports = html.xpath('//*[@class="table table-hover table-bordered"]/tbody/tr/td[2]/text()')
            styles = html.xpath('//*[@class="table table-hover table-bordered"]/tbody/tr/td[5]/text()')
            ips_time = html.xpath('//*[@class="table table-hover table-bordered"]/tbody/tr/td[8]/text()')
            t = time.time()
            countrys = html.xpath('//*[@class="table table-hover table-bordered"]/tbody/tr/td[3]/a[1]/text()')
            if ips and ports and styles and ips_time and countrys:
                for ip, port, style, country in zip(ips, ports, styles, countrys):
                    if '中国' in country:  # 提取中国地区的高匿
                        style = 'https' if '支持' in style else 'http'
                        item = ','.join([str(ip), str(port), style.lower(), str(int(t)), '0', '0'])
                        ips_list.append(item)
            sign = self.get_item(ips_list, spider_name='ihuan')  # 增量信号到达判断
            k += 1
            if k > 100:  # 每过一段时间爬取一次首页
                break
            time.sleep(5)

    def get_item(self, ips, spider_name):
        """多线程验证ips"""
        if spider_name == 'xici':
            latest_time = self.latest_time['xici']
        if spider_name == 'kuaidaili':
            latest_time = self.latest_time['kuaidaili']
        if spider_name == 'ihuan':
            latest_time = self.latest_time['ihuan']
        if spider_name == 'ip3366':
            latest_time = self.latest_time['ip3366']
        pool = ThreadPoolExecutor(max_workers=100)
        for line in ips:
            line_list = line.rstrip().split(',')
            ip, port, style = line_list[0], line_list[1], line_list[2]
            ip_time, connect, success = str(int(line_list[3])), str(int(line_list[4])), str(int(line_list[5]))

            if int(ip_time) > int(latest_time):
                pass
            else:
                return True
            item = ','.join([ip, port, style, ip_time, connect, success])
            pool.submit(self.check_ip, item, spider_name)
        pool.shutdown()
        return False

    def check_ip(self, item, spider_name):
        """验证单个ip代理"""
        line_list = item.rstrip().split(',')
        ip, port, style = line_list[0], line_list[1], line_list[2]
        ip_time, connect, success = int(line_list[3]), int(line_list[4]), int(line_list[5])

        headers = {'User-Agent': random.choice(USER_AGENT)}
        proxy = {}
        if style == 'http':
            proxy = {'http': 'http://{0}:{1}'.format(ip, port)}
            url = 'http://httpbin.org/get?show_env=1'
        if style == 'https':
            proxy = {'https': 'https://{0}:{1}'.format(ip, port)}
            url = 'https://httpbin.org/get?show_env=1'
        req = request.Request(url, headers=headers)
        opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxy))
        try:
            resp = opener.open(req, timeout=5)
            if resp.status == 200:
                html = str(resp.read(), encoding='utf8')
                if ip in html:
                    connect += 1
                    success += 1
                    items = ','.join([ip, port, style, str(ip_time), str(connect), str(success)])
                    self.ips_useful.add(items)

                    print(items)
                    if spider_name == 'xici':
                        if ip_time > self.latest_useful['xici']:
                            self.latest_useful['xici'] = ip_time
                    if spider_name == 'kuaidaili':
                        if ip_time > self.latest_useful['kuaidaili']:
                            self.latest_useful['kuaidaili'] = ip_time
                    if spider_name == 'ihuan':
                        if ip_time > self.latest_useful['ihuan']:
                            self.latest_useful['ihuan'] = ip_time
                    if spider_name == 'ip3366':
                        if ip_time > self.latest_useful['ip3366']:
                            self.latest_useful['ip3366'] = ip_time

                    if style == 'http':
                        self.proxy_list.append(proxy)
                        self.proxy = self.proxy_list[-1]
            else:
                print(resp.status)
        except Exception as e:
            connect += 1

        # time_local = time.localtime(ip_time)  # 转换成localtime
        # dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 转换成新的时间格式(2018-05-05 20:28:54)
        # itemss = ','.join([ip, port, style, str(ip_time), str(connect), str(success)])
        # print(dt, itemss)

    def write_text(self):
        """最后将有效代理写入文件"""
        with open('poolproxy.txt', 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.latest_useful))
            f.write('\n')
        for line in list(set(self.file_list) | self.ips_useful):
            with open('poolproxy.txt', 'a', encoding='utf-8') as af:
                af.write(line + '\n')

    def run(self):
        """主逻辑"""
        self.read_file()
        self.get_ips_xici()
        self.write_text()

        self.get_ips_ip3366()
        self.write_text()

        self.get_ips_kuaidaili()
        self.write_text()

        self.get_ips_ihuan()
        self.write_text()


if __name__ == '__main__':
    tt = PoolProxy()
    tt.run()

    # 程序后台运行
    # nohup python -u time1.py >poolproxy.log 2>&1 &
    # 实时log显示
    # tail -f poolproxy.log
