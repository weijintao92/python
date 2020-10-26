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
from fake_useragent import UserAgent  # 爬虫请求头伪装

# import parse  # 用于计算时间差
# import atexit #脚本退出时执行的函数

# ip_pools_path = "proxies\ip_proxy\kuaidaili_ip_pools.txt"
ip_list = []  # 代理IP集合
begin_page_number = 0  # 代理IP源开始爬取页码
list_page_number = []  
next_url = ''   #百度搜索，下一页url
is_tasks = False #是否结束任务


# 脚本结束时将，内存中剩余的代理ip写会文本中
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
    # 提取一个url
    proxies = {
        "http": "http://"+proxies_ip,   # http  型的
        "https": "http://"+proxies_ip   # https 型的
    }

    try:
        ua = UserAgent()  # 爬虫请求头伪装
        # 目前会抛出ConnectionError错误，目前的解决方案是捕获并跳过此异常，继续任务
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
        # 百度的url也需要组装
        # r = requests.get('https://www.baidu.com/s?ie=UTF-8',
        #                  params=my_params, headers=my_headers, timeout=5, proxies=proxies, verify=False)
        global next_url
        if next_url !='':
            r = requests.get(url=next_url, headers=my_headers, timeout=5, proxies=proxies, verify=False)
            print("下一页")
            if r.status_code == 200:
            # 如果这个代理ip有效就多用几次
            global ip_list
            ip_list.append(proxies_ip)
            time.sleep(2)
            
            print(proxies_ip+"成功！\n")
            # aa=r.content.decode('utf-8')
            # ss = r.text.replace('\n','').replace('\t','').replace('\r','')

            #开始解析数据
            soup = BeautifulSoup(r.text, "html.parser")
            # print(soup)
            #提取页码，已放弃
            # for item in soup.find_all('div', class_="page-inner"):
            #     for item2 in item.find_all('a'):
            #         if item2.get_text() != '< 上一页':
            #             list_page_number.append({'number': item2.get_text(
            #             ), 'number_url': 'https://www.baidu.com'+item2.get('href')})
            #获取百度搜索下一页的跳转地址,并猜测此关键字可能的页码长度，组装页码集合
            #循环遍历根据页码集合，创建线程。并将失败的页码添加到另一个集合中，再次循环遍历创建线程。至到，所有页码请求成功。
            #判断页码集合实际长度，并修正失败页码集合的长度。
            next_soup = soup.find_all('a',text="下一页 >")
            #如果没有找到下一页的标签，表示页码已经到底了
            if len(next_soup)==0:
                print('结束任务！')
                global is_tasks
                is_tasks = True
                #获取当前页码
                begin_index=next_url.find('pn=')
                end_index = next_url.find('&oq')
                next_url[begin_index+3:end_index]
            next_url = 'https://www.baidu.com'+next_soup[0].get("href")

            # 1.获取内容
            list_page = []
            tags_page = soup.find_all(attrs={"srcid": "1599"} )
            for item in tags_page:
                # print(item)
                #获取名称
                list_name = item.h3.find_all('a')
                name = list_name[0].get_text()
                href = list_name[0].get('href')
                #获取描述
                list_descript= item.find_all('div',class_="c-abstract c-abstract-en")
                descript = list_descript[0].get_text()
                #组装数据
                list_page.append({'name':name,'href':href,'descript':descript})
        else:
            r = requests.get(
            'https://www.baidu.com/s?ie=UTF-8&wd=free%20sxe%20jva', headers=my_headers, timeout=5)    
            print('第一次')
            #开始解析数据
            soup = BeautifulSoup(r.text, "html.parser")
            next_soup = soup.find_all('a',text="下一页 >")
            #如果没有找到下一页的标签，表示页码已经到底了
            if len(next_soup)==0:
                
    except Exception:
        # list_page_number.append(url)
        print(proxies_ip+"超时！\n")
        # 如果超时，将页码url重写回list集合中
    else:
        pass
    finally:
        pass


class myThread1(threading.Thread):
    def __init__(self, proxies_ip):
        threading.Thread.__init__(self)
        self.proxies_ip = proxies_ip
    def run(self):
        # print("开始线程：" + self.proxies_ip+"\n")
        get_baidu_wd('free sxe jva',self.proxies_ip)


def newmethod304():
    global ip_list
    global begin_page_number
    while 1 == 1:
        #是否结束任务
        if is_tasks:
            break
        #是否需要抓取代理IP
        if len(ip_list) == 0:
            time.sleep(1)
            ip_list = parsing_html.get_kuaidaili_free_ip(begin_page_number)
        #开始任务
        while len(ip_list) != 0:
            #获取代理IP
            proxies_ip = ip_list.pop()  # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            # 创建新线程
            myThread1(proxies_ip).start()
        begin_page_number += 1
    print("任务结束！")

if __name__ == '__main__':
    newmethod304()
    # # 123.163.115.180:9999
    # get_baidu_wd('free sxe jva', '123.163.115.180:9999')
    # get_baidu_wd('free sxe jva', '123.163.115.180:9999')
    # get_baidu_wd('free sxe jva', '123.163.115.180:9999')


# 根据url搜索
def get_baidu_url(my_url):
    # 定制请求头
    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
        'Accept': '*/*'
    }
    # 获取代理IP
    list_pop = ip_list.pop()  # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
    proxies = {
        "http": "http://"+list_pop,   # http  型的
        "https": "http://"+list_pop   # https 型的
    }
    resoult = requests.get(my_url, headers=my_headers, proxies=proxies)
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
# 获取代理IP集合
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
    # 读取ip地址，写入全局集合中ip_list

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
