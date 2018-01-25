import requests
import time
from bs4 import BeautifulSoup
import re


def urlGetHtml(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("url_get Error")


def htmlGetList(htmltext, list):
    soup = BeautifulSoup(htmltext, "html.parser")
    tbody = soup.find("tbody")
    tr = tbody("tr")
    for j in range(len(tr)):
        tds = tr[j].td
        tx = re.search(r'\d{1,3}', tds.text)
        list.append(tx.group(0))
        td = tds("td")
        for i in range(len(td)):
            list.append(td[i].string)

    return list


def listToPrint(rlist, path):
    list = []
    for i in range(0, len(rlist), 13):
        list1 = []
        for j in range(0, 13):
            list1.append(rlist[i + j])
        list.append(list1)
    rule = re.compile(r'[\'\]\[]')
    with open(path, 'w') as file:
        list1 = ['排名', '学校名称', '省市', '总分', '生源质量（新生高考成绩得分）',
                 '培养结果（毕业生就业率）', '科研规模（论文数量·篇）', '科研质量（论文质量·FWCI）',
                 '顶尖成果（高被引论文·篇）', '顶尖人才（高被引学者·人）', '科技服务（企业科研经费·千元）',
                 '成果转化（技术转让收入·千元）', '学生国际化（留学生比例）']
        list.insert(0, list1)
        for i in range(len(list)):
            li = str(list[i])
            li = rule.sub('', li)
            file.writelines(li + '\n')


if __name__ == '__main__':
    url = "http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html"
    path = 'C:/Users/wzq/Desktop/中国大学排名数据.csv'
    list = []
    a = time.time()
    listToPrint(htmlGetList(urlGetHtml(url), list), path)
    print('Time:%s' % (time.time() - a))
