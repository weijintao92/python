#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
# import re #正则表达式
import json
import time
# import datetime
# import threading  # 多线程
# import os  # 文件操作
from fake_useragent import UserAgent  # 爬虫请求头伪装
# 导入 random(随机数) 模块
import random
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)  # 禁止https(ssl)问题的报错


#验证链接可用性，无法响应的直接干掉
def check_url():
    """
    验证url可用性
    """
    #
    with open('aaa.txt', "r") as fs:
        json_url = fs.read()
        fs.close()

    list_url = json.loads(json_url)
    list_true = []
    list_ConnectionError =[]
    while len(list_url) >0:

        try:
            ua = UserAgent()  # 爬虫请求头伪装
            # 目前会抛出ConnectionError错误，错误1：目标网站访问超时
            # 未解决定制请求头的问题，目前思考的是完全模拟请求头里的所有参数（未验证此方法的可行性）

            # 定制请求头
            my_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'BIDUPSID=168C7F2BA03828C13272D6BE432D667A; PSTM=1603554287; BAIDUID=168C7F2BA03828C1B773A6F551E13C63:FG=1; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_PSSID=1447_32844_31660_32723_32230_7516_7605_32115_31708_26350; BD_UPN=12314753; H_PS_645EC=1e7a9EZYBbpG7jVqrrlfiTQfF0KcYUoJLc3nd9Fa7goUgyqHuxQAB358Afc; BA_HECTOR=al85al842ga18008ua1fp8iug0k; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598',
                'Host': 'www.baidu.com',
                'Referer': 'https://www.baidu.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': ua.chrome,
            }
            list_item_url = list_url.pop()
            url = list_item_url['href']
            r = requests.get(url=url, headers=my_headers,timeout=5, verify=False)
            true_url = r.url
            text = r.text
            #输出任务进度

            print(len(list_url))
            if r.status_code == 200:
                # list_true.append(list_item_url)
                list_true.append({'name':list_item_url['name'],'href':r.url,'descript':list_item_url['descript']})
                #输出
                oupput_check_ok(list_true)
            else:
                print('超时'+url)
                #采集失败的url
                list_ConnectionError.append(list_item_url)
                #输出
                oupput_ConnectionError(list_ConnectionError)
            
            #随机休眠3-9秒
            time.sleep(random.randint(3,9))
        # #重定向次数太多了
        # except (requests.exceptions.TooManyRedirects):
        #     print('目标网站访问超时！')
        #     #采集失败的url
        #     list_ConnectionError.append(list_item_url)
        #     #输出
        #     oupput_ConnectionError(list_ConnectionError)
        # #超时了
        # except (requests.exceptions.ConnectionError,requests.exceptions.ReadTimeout):
        #     print('目标网站访问超时！')
        #     #采集失败的url
        #     list_ConnectionError.append(list_item_url)
        #     #输出
        #     oupput_ConnectionError(list_ConnectionError)
        except Exception:
            print('目标网站访问超时！')
            #采集失败的url
            list_ConnectionError.append(list_item_url)
            #输出
            oupput_ConnectionError(list_ConnectionError)
        

def oupput_check_ok(my_lists = []):
    """
    任务进行中的错误日志
    """
    with open('check_ok.txt', "w") as fs:
        fs.write(json.dumps(my_lists))
        fs.close()

#采集所有错误
def oupput_ConnectionError(my_lists = []):
    """
    任务进行中的错误日志
    """
    with open('ConnectionError.txt', "w") as fs:
        fs.write(json.dumps(my_lists))
        fs.close()

if __name__ == '__main__':
    check_url()
    # main_proxies_thread()
    # # 123.163.115.180:9999
    # get_baidu_wd('free sxe jva', '123.163.115.180:9999','')
            