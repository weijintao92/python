#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import datetime
import threading  # 多线程
import os  # 文件操作
import proxies.parsing_html as parsing_html
from fake_useragent import UserAgent #爬虫请求头伪装

# import parse  # 用于计算时间差
# import atexit #脚本退出时执行的函数
  
# ip_pools_path = "proxies\ip_proxy\kuaidaili_ip_pools.txt" 
ip_list =[]  #代理IP集合
begin_page_number = 0  #代理IP源开始爬取页码


#脚本结束时将，内存中剩余的代理ip写会文本中
# @atexit.register 
# def clean_1(): 
#   with open(ip_pools_path, "w") as fs:
#         for i in range(len(ip_list)):
#             fs.write(ip_list[i])
#         fs.close()
#         print("回写剩余IP成功！")
#         fs.close()

# pat = re.compile("abc")
# m= pat.search("abcd")
# print(m)


# def main():
#     my_url = "https://www.baidu.com/s?ie=UTF-8"

# findLink = re.compile()   #正则表达式

# # 爬取网页


# def getData(my_url):

#     # 构建查询条件
# my_params = {'wd': 'free sxe jva'}
# # 定制请求头
# my_headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
#     'Accept': '*/*'
# }
# r = requests.get('https://www.baidu.com/s?ie=UTF-8',
#                  params=my_params, headers=my_headers)
# # 保存原网页至文件
# with open('baidu.html', 'wb') as fd:
#     for chunk in r.iter_content(chunk_size=1024):
#         fd.write(chunk)

# 根据关键字搜索
def get_baidu_wd(my_wd,proxies_ip):

    # 判断全局list集合中是否存在页码url
    #提取一个url
    # 构建查询条件
    my_params = {'wd': my_wd}
    
    proxies = {
        "http": "http://"+proxies_ip,   # http  型的
        "https": "http://"+proxies_ip   # https 型的
    }

    try:
        ua = UserAgent() #爬虫请求头伪装
        # 目前会抛出ConnectionError错误，目前的解决方案是捕获并跳过此异常，继续任务
        # 未解决定制请求头的问题，目前思考的是完全模拟请求头里的所有参数（未验证此方法的可行性）
        # 未解决 多线程日志输入换行的问题
        # 定制请求头
        my_headers = {
            "User-Agent":ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
        }  
        r = requests.get('https://www.baidu.com/s?ie=UTF-8',
                           params=my_params, headers=my_headers,proxies = proxies,timeout=2, verify=False)
    except (requests.exceptions.ConnectTimeout,requests.exceptions.ProxyError,Exception):
        print(proxies_ip+"超时！")
        # 如果超时，将页码url重写回list集合中
    else:
        if r.status_code == 200:
            print(proxies_ip+"成功！")
            # 1.获取内容
                # 1.1 剔除重复，写入临时list集合
                # 1.2 检测延迟
                # 1.3 写入全局 list 集合
                # 1.4 调用装饰器，程序关闭时，将list集合中现有数据输出至excle
            # 2.获取当前页索引
            #2.1 写入临时list集合
            # 2.2 判断是否到最后一页了，销毁所有线程

    finally:
        pass
    
    
#

def newmethod304():
    global ip_list
    global begin_page_number
    while 1==1:
        if len(ip_list) == 0:
            time.sleep(1)
            ip_list = parsing_html.get_kuaidaili_free_ip(begin_page_number)
        while len(ip_list) !=0:
            proxies_ip = ip_list.pop().replace('\n','') #移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            # 创建新线程
            myThread1(proxies_ip).start()
            
        begin_page_number+=1   

       
# 根据url搜索
def get_baidu_url(my_url):
     # 定制请求头
    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
        'Accept': '*/*'
    }
    #获取代理IP
    list_pop = ip_list.pop() #移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
    proxies = {
        "http": "http://"+list_pop,   # http  型的
        "https": "http://"+list_pop   # https 型的
    }
    resoult = requests.get(my_url, headers=my_headers,proxies=proxies)
    return resoult.text


# my_file = open(r".\baidu.html", 'rb')
# my_html = my_file.read()
# my_soup = BeautifulSoup(my_html, "html.parser")
# for item in my_soup.find_all('div',class_="c-tools"):   #查找符合要求的内容
#     print(item)
#     # print(item.get('data-tools'))
#     # data2 = json.loads(item.get('data-tools'))
#     # print ( data2['title'],data2['url'])


# 开始抓取任务
def my_main():
    list_data = []
    list_temp = []
    my_bool = 'true'
    temp_url = ''
    while my_bool == 'true':
        if len(list_data) == 0:
            resoult = get_baidu_wd('free sxe jva')
        else:
            resoult = get_baidu_url(page_url)
        my_soup = BeautifulSoup(resoult, "html.parser")
        for item in my_soup.find_all('div', class_="page-inner"):
            for item2 in item.find_all('a'):
                if item2.get_text() != '< 上一页':
                    list_temp.append({'number': item2.get_text(
                    ), 'number_url': 'https://www.baidu.com'+item2.get('href')})
        if len(list_temp) >= 9:
            # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
            list_pop = list_temp.pop()
            if list_pop['number'] != "下一页 >":
                my_bool = 'false'
                list_temp.append(list_pop)
            list_data = list_data+list_temp
            page_url = list_pop['number_url']
            list_temp.clear()
            # print(datetime.datetime.now())
            time.sleep(0.1)
#获取代理IP集合
# def get_proxies_ip(ip_pools_path):
    # now_time = time.strftime("%Y-%m-%d %H:%M:%S") # 当前日期
    # a = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    # # print(time.ctime(os.path.getctime("proxies/ip_proxy/2020_10_22_ip_pools.txt")) )
    # # 获取文件修改日期，并转换成localtime
    # time_local = time.localtime(os.path.getmtime("proxies/ip_proxy/kuaidaili_ip_pools.txt"))
    # # 转换成新的时间格式(2016-05-05 20:28:54)
    # create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    # b = datetime.datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    # # print((a-b).seconds/60)
    # print((a-b).seconds)
    # time_interval=(a-b).seconds/3600
    # #如果获取的代理ip文件时间间隔超过4小时，就重新获取代理ip
    # if time_interval>4:
    #     #获取新的代理IP
    #     parsing_html.get_kuaidaili_free_ip('',ip_pools_path,False)
    #读取ip地址，写入全局集合中ip_list
    
    # with open(ip_pools_path, "r") as fr:  
    #     ip_list = fr.readlines()
    #     fr.close()
    
        # #读取ip地址，写入全局集合中ip_list
        # with open(ip_pools_path, "r") as fr:
        #     ip_list = fr.readlines()
        #     fr.close()
    
    
    # else:
    #     # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
    #     list_pop = list_temp.pop()
    #     list_data = list_data+list_temp
    #     my_bool = 'false'

# for target_list in list_data:
#     print(target_list['number'])

class myThread1(threading.Thread):
    def __init__(self,proxies_ip):
        threading.Thread.__init__(self)
        self.proxies_ip = proxies_ip
    def run(self):
        print("开始线程：" + self.proxies_ip)
        get_baidu_wd('free sxe jva',self.proxies_ip)  


if __name__ == '__main__':
    newmethod304()

    

# if __name__ == "__main__":
#     # get_proxies_ip(ip_pools_path)
#     newmethod304()

# print(today)
# ip_pools_path = "proxies\ip_proxy\\" + today + "_ip_pools.txt"
# get_kuaidaili_free_ip('',ip_pools_path,False)


# for item in my_soup.find_all('div', class_="page-inner"):
#     for item2 in item.find_all('a'):
#         # print(item2.get_text())
#         # print('https://www.baidu.com'+item2.get('href'))
#         if item2.get_text() != '下一页 >' and item2.get_text() != '< 上一页':
#             list_data.append({'number': item2.get_text(
#             ), 'number_url': 'https://www.baidu.com'+item2.get('href')})
#         elif item2.get_text() == '下一页 >':
#             list_next.append({'number': item2.get_text(
#             ), 'number_url': 'https://www.baidu.com'+item2.get('href')})

# # 遍历列表
# for target_list in list_data:
#     print(target_list['number'])
# print('-----------------------------------------')
# for target_list in list_next:
#     print(target_list['number'])
