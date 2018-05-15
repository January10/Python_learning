#!/D:/python/Anaconda/python.exe
# coding:utf-8
__author__ = 'wzq'

import requests
import re


def jobLogin():
    # sesion保存信息
    session = requests.session()

    # headers
    # agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "51job-android-client",
        "Connection": "Keep-Alive",
        "Host": "api.51job.com"
    }

    keyword = 'python'
    pagesize = 30
    response = session.get(
        'http://api.51job.com/api/job/search_job_list.php?postchannel=0000&&keyword={0}&keywordtype=2&jobarea=070200\
        &pageno=1&pagesize={1}&accountid=138768567&key=7e723e0dec8bbdc5109d2869ff65a0fd5af1a83c&productname=51job&\
        partner=20e365d3297df231e3b0c4100e8b14b7&uuid=82db8436a5ade5336ab0cb06c58fafe3&version=821&\
        guid=56bf94e874783938110a01e31c1e28c5'.format(keyword, pagesize), headers=headers)
    # &workyear=01,05&|&issuedate=0到3&
    r = response.text
    # print(r)
    totalcount_str = re.findall(r'count>(\d+)</total', r)[0]
    # print(int(totalcount_str))
    pagesize = int(totalcount_str)
    resp = session.get(
        'http://api.51job.com/api/job/search_job_list.php?postchannel=0000&&keyword={0}&keywordtype=2&jobarea=070200\
        &pageno=1&pagesize={1}&accountid=138768567&key=7e723e0dec8bbdc5109d2869ff65a0fd5af1a83c&productname=51job&\
        partner=20e365d3297df231e3b0c4100e8b14b7&uuid=82db8436a5ade5336ab0cb06c58fafe3&version=821&\
        guid=56bf94e874783938110a01e31c1e28c5'.format(keyword, pagesize), headers=headers)


if __name__ == "__main__":
    jobLogin()
