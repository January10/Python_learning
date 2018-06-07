'''to get ips_pool'''

import asyncio, aiomysql, logging
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.INFO)


def log(args):
    logging.info(args)


def geturls():
    urls = []
    for i in range(1, 2600):  # 1-2695
        url = 'http://www.xicidaili.com/nn/{}'.format(i)
        urls.append(url)
    return urls


@asyncio.coroutine
def spider_ips(urls, queue):
    for url in urls:
        options.get(url)  # 打开链接
        options.implicitly_wait(10)  # 隐式等待10S
        selector = etree.HTML(options.page_source)
        infos = selector.xpath('//*[@id="ip_list"]/tbody')
        for info in infos:
            ip = info.xpath('tr[@class]/td[2]/text()')
            port = info.xpath('tr[@class]/td[3]/text()')
            dict = {
                'ip': ip,
                'port': port
            }
            # log(dict.items())
        yield from queue.put(dict)
        yield from asyncio.sleep(1)
    yield from queue.put(None)


@asyncio.coroutine
def tomysql(queue):
    while 1:
        dict = yield from queue.get()
        if dict is None:
            break
        conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, charset='utf8', autocommit=True,
                                           user='root', password='root',
                                           db='testdb', loop=loop)
        cur = yield from conn.cursor()
        yield from cur.execute(
            "create table if not exists testdb.spider_ips(ID int unsigned not null auto_increment primary key,\
            ip varchar(244) not null,\
            port varchar(244) not null)")
        for i in range(len(dict['ip'])):
            yield from cur.execute('insert into testdb.spider_ips(ip,port) values(%s,%s)',
                                   (dict['ip'][i], dict['port'][i]))
            log([dict['ip'][i], dict['port'][i]])
        yield from cur.close()
        conn.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue(loop=loop)  # 创建队列
    consumer = asyncio.ensure_future(tomysql(queue))

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=zh_CN.UTF-8')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 无图模式
    options = webdriver.Chrome(chrome_options=chrome_options)  # 启动浏览器
    options.maximize_window()  # 最大化窗口

    urls = geturls()
    loop.run_until_complete(asyncio.gather(spider_ips(urls, queue), tomysql(queue)))
    loop.close()
    options.close()  # 关闭浏览器
