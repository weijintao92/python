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
import json
# 导入 random(随机数) 模块
import random
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
 
disable_warnings(InsecureRequestWarning)  # 禁止https(ssl)问题的报错
 


# import parse  # 用于计算时间差
# import atexit #脚本退出时执行的函数

# ip_pools_path = "proxies\ip_proxy\kuaidaili_ip_pools.txt"
ip_list = []  # 代理IP集合
begin_page_number = 0  # 代理IP源开始爬取页码
list_page_number = []  
next_url = ''   #百度搜索，下一页url
is_tasks = False #是否结束任务
#构造查询页码，假定页码有100页
list_hypothesis_page = []
#第一次抓取是否成功
is_first_bool = True
#内容
list_page = []


# 脚本结束时将内存中抓取的内容输出至excel
# @atexit.register
# def out_excel():
#   with open('ff.txt', "w") as fs:
#         for i in range(len(list_page)):
#             fs.write(list_page[i]+'\n')
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

# 根据关键字搜索，启用代理
def get_proxies_wd(proxies_ip,my_wd):
    global list_hypothesis_page 
    global is_first_bool
    # 组装搜索条件
    payload = {'wd': my_wd}
    
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
        #第一次抓取
        r = requests.get(
        'https://www.baidu.com/s?ie=UTF-8',params=payload,  headers=my_headers, timeout=5, proxies=proxies, verify=False)
        print('第一次'+r.url)
        # 设置线程锁
        threadLock = threading.Lock()
        #开始解析数据
        soup = BeautifulSoup(r.text, "html.parser")
        next_soup = soup.find_all('a',text="下一页 >")
        #如果没有找到下一页的标签，应该时被目标网站检测出是爬虫了
        if len(next_soup)==0:
            print('结束任务！')
            # is_tasks = True
            raise Exception('任务开始时失败了！')
        next_url = 'https://www.baidu.com'+next_soup[0].get("href")
        #构造查询页码，假定页码有100页
        temp_index = 10
        begin_index=next_url.find('pn=')
        end_index = next_url.find('&oq')
        threadLock.acquire()
        while temp_index<=1000:
            list_hypothesis_page.append(next_url[0:begin_index+3]+ str(temp_index) +next_url[end_index:len(next_url)])
            temp_index=temp_index+10
        #将列表里面将元素进行逆序排列
        list_hypothesis_page.reverse()
        #将url输出到文本，用于测试
        with open('url_json.txt', "w") as fs:
            fs.write(json.dumps(list_hypothesis_page))
            fs.close()
        #标记第一次任务
        is_first_bool= False

        # 1.获取内容
        global list_page
        tags_page = soup.find_all(attrs={"srcid": "1599"} )
        for item in tags_page:
            #获取名称
            name=''
            href=''
            list_name = item.h3.find_all('a')
            name = list_name[0].get_text()
            href = list_name[0].get('href')
            #获取描述    c-abstract
            descript=''
            list_descript= item.find_all('div',class_="c-abstract c-abstract-en")
            list_descript= item.find_all('div',class_="c-abstract")
            if len(list_descript) !=0:
                descript = list_descript[0].get_text()
            #组装数据
            list_page.append({'name':name,'href':href,'descript':descript})
        #输出一次内容
        with open('aaa.txt', "w") as fs:
                fs.write(json.dumps(list_page))
                fs.close()
                    
        # 如果这个代理ip有效就多用几次
        global ip_list
        ip_list.append(proxies_ip)
        # 释放锁
        threadLock.release()
        time.sleep(1)
        # print(proxies_ip+"第一次成功！\n")       
    except requests.exceptions.ProxyError:
        print('代理出错了！')
    except Exception:
        # list_page_number.append(url)
        print(proxies_ip+"第一次超时！\n")
        # 如果超时，将页码url重写回list集合中
        # list_hypothesis_page.append(next_url)
    else:
        pass
    finally:
        pass

# 根据关键字搜索，没有启用代理
def get_wd(my_wd):
    global list_hypothesis_page 
    global is_first_bool
    # 组装搜索条件
    payload = {'wd': my_wd}

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
        #第一次抓取
        r = requests.get(
        'https://www.baidu.com/s?ie=UTF-8',params=payload, headers=my_headers, timeout=5, verify=False)

        print('第一次'+r.url)
        #开始解析数据
        soup = BeautifulSoup(r.text, "html.parser")
        list_next = soup.find_all('a',text="下一页 >")
        list_items = soup.find_all(attrs={"srcid": "1599"} )
        #如果没有找到下一页的标签，会有2种情况：第一种：任务失败了，目标网站返回结果异常。第二种：已经到最后一页了
        if len(list_next)==0 and len(list_items)==0:  
            oupput_reptile_log(r.url+"第一次请求时任务失败！，目标网站返回结果异常！")
            print("第一次请求时任务失败！，目标网站返回结果异常！")
            return 
        #判断是否已经到最后一页了
        if len(list_next)>0:
            #构造url集合，假定页码有100页
            next_url = 'https://www.baidu.com'+list_next[0].get("href")
            temp_index = 10
            begin_index=next_url.find('pn=')
            end_index = next_url.find('&oq')

            while temp_index<=1000:
                list_hypothesis_page.append(next_url[0:begin_index+3]+ str(temp_index) +next_url[end_index:len(next_url)])
                temp_index=temp_index+10
            #将列表里面将元素进行逆序排列
            list_hypothesis_page.reverse()
            #将url集合输出到文本
            with open('url_json.txt', "w") as fs:
                fs.write(json.dumps(list_hypothesis_page))
                fs.close()
            #标记第一次任务
            is_first_bool= False
            print('构造url集合，假定页码有100页!任务成功！')
            time.sleep(3)

        # 获取内容
        global list_page
        tags_page = soup.find_all(attrs={"srcid": "1599"} )
        for item in tags_page:
            #获取名称
            name=''
            href=''
            list_name = item.h3.find_all('a')
            name = list_name[0].get_text()
            href = list_name[0].get('href')
            #获取描述    c-abstract
            descript=''
            list_descript= item.find_all('div',class_="c-abstract c-abstract-en")
            list_descript= item.find_all('div',class_="c-abstract")
            if len(list_descript) !=0:
                descript = list_descript[0].get_text()
            #组装数据
            list_page.append({'name':name,'href':href,'descript':descript})
        #输出一次内容
        with open('aaa.txt', "w") as fs:
                fs.write(json.dumps(list_page))
                fs.close()
         
    except requests.exceptions.ProxyError:
        print('代理出错了！')
    except Exception:
        # list_page_number.append(url)
        print("第一次超时！\n")
        # 如果超时，将页码url重写回list集合中
        # list_hypothesis_page.append(next_url)
    else:
        pass
    finally:
        pass

# 根据url集合搜索
def get_proxies_url(proxies_ip,url):
    global list_hypothesis_page 
    
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
        
        if url !='':
            r = requests.get(url=url, headers=my_headers, timeout=5, proxies=proxies, verify=False)
            print("下一页")
            # 设置线程锁
            threadLock = threading.Lock()
            if r.status_code == 200:
                #开始解析数据
                soup = BeautifulSoup(r.text, "html.parser")
                #判断页码集合实际长度，并修正失败页码集合的长度。
                next_soup = soup.find_all('a',text="下一页 >")
                #如果没有找到下一页的标签，应该时被目标网站检测出是爬虫了
                if len(next_soup)==0:
                    raise Exception('任务开始时失败了，目标网站返回结果异常！')
                next_url_temp = 'https://www.baidu.com'+next_soup[0].get("href")
                a_index=next_url_temp.find('pn=')
                b_index = next_url_temp.find('&oq')
                pn_new = int(next_url_temp[a_index+3:b_index])
                #如果索引超出了上限，目标网站会返回首页,那么就结束当前线程不要向下执行了。同时，线程锁定list_hypothesis_page集合，清空集合之后的所有元素
                begin_index=url.find('pn=')
                end_index = url.find('&oq')
                pn_old = int(url[begin_index+3:end_index])
                if pn_old+10 != pn_new:
                    print("清理url集合！")
                    threadLock = threading.Lock()
                     # 获取锁，用于线程同步
                    threadLock.acquire()
                    while pn_old<=len(list_hypothesis_page)*10:
                        pn_old+=10
                        list_hypothesis_page.remove(url[0:begin_index+3]+ pn_old +url[end_index:len(url)])
                    # 释放锁
                    threadLock.release()
                    return
        # 1.获取内容
        threadLock.acquire()
        global list_page
        tags_page = soup.find_all(attrs={"srcid": "1599"} )
        for item in tags_page:
            #获取名称
            name=''
            href=''
            list_name = item.h3.find_all('a')
            name = list_name[0].get_text()
            href = list_name[0].get('href')
            #获取描述    c-abstract
            descript=''
            list_descript= item.find_all('div',class_="c-abstract c-abstract-en")
            list_descript= item.find_all('div',class_="c-abstract")
            if len(list_descript) !=0:
                descript = list_descript[0].get_text()
            #组装数据
            list_page.append({'name':name,'href':href,'descript':descript})
        #输出一次内容
        with open('aaa.txt', "w") as fs:
            fs.write(json.dumps(list_page))
            fs.close()
        # 如果这个代理ip有效就多用几次
        global ip_list
        ip_list.append(proxies_ip)
        # 释放锁
        threadLock.release()
        time.sleep(1)
        # print(proxies_ip+"成功！\n")       
    except Exception :
        # list_page_number.append(url)
        # print(Exception)
        print(proxies_ip+"url超时！\n")
        # 如果超时，将页码url重写回list集合中
        list_hypothesis_page.append(url)   
    else:
        pass
    finally:
        pass

#输出日志
def oupput_reptile_log(my_text):
    """
    任务进行中的错误日志
    """
    with open('reptile_log.txt', "a+") as fs:
        fs.write(my_text+'\n')
        fs.close()

# 根据url集合搜索
def get_url(url):
    global list_hypothesis_page 
    
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
        
        if url !='':
            r = requests.get(url=url, headers=my_headers,timeout=5, verify=False)

            print("url请求成功！")

            if r.status_code == 200:
                #开始解析数据
                soup = BeautifulSoup(r.text, "html.parser")
                list_next = soup.find_all('a',text="下一页 >")
                list_items = soup.find_all(attrs={"srcid": "1599"} )
                #如果没有找到下一页的标签，回有2种情况：第一种：任务失败了，目标网站返回结果异常。第二种：已经到最后一页了
                if len(list_next)==0 and len(list_items)==0:
                    list_hypothesis_page.append(url)   
                    oupput_reptile_log(url+"url任务失败！，目标网站返回结果异常！")
                    print("url任务失败！，目标网站返回结果异常！")
                    return 
                #已经到最后一页了
                if len(list_next)==0:
                    #清空模拟的url集合，结束任务
                    list_hypothesis_page.clear()
                    print('已经到最后一页了，任务即将结束！')
                    time.sleep(3)
                # next_url_temp = 'https://www.baidu.com'+list_next[0].get("href")
                # a_index=next_url_temp.find('pn=')
                # b_index = next_url_temp.find('&oq')
                # pn_new = int(next_url_temp[a_index+3:b_index])
                # #如果索引超出了上限，目标网站会返回首页,那么就结束当前线程不要向下执行了。同时，线程锁定list_hypothesis_page集合，清空集合之后的所有元素
                # begin_index=url.find('pn=')
                # end_index = url.find('&oq')
                # pn_old = int(url[begin_index+3:end_index])
                # if pn_old+10 != pn_new:
                #     print("修正url集合！")
                #     while pn_old<=len(list_hypothesis_page)*10:
                #         pn_old+=10
                #         list_hypothesis_page.remove(url[0:begin_index+3]+ pn_old +url[end_index:len(url)])
                #     return
        # 1.获取内容
        global list_page
        tags_page = soup.find_all(attrs={"srcid": "1599"} )
        for item in tags_page:
            #获取名称
            name=''
            href=''
            list_name = item.h3.find_all('a')
            name = list_name[0].get_text()
            href = list_name[0].get('href')
            #获取描述    c-abstract
            descript=''
            list_descript= item.find_all('div',class_="c-abstract c-abstract-en")
            list_descript= item.find_all('div',class_="c-abstract")
            if len(list_descript) !=0:
                descript = list_descript[0].get_text()
            #组装数据
            list_page.append({'name':name,'href':href,'descript':descript})
        #输出一次内容
        with open('aaa.txt', "w") as fs:
            fs.write(json.dumps(list_page))
            fs.close()
             
    except Exception :
        print('url出错了')
        # 如果超时，将页码url重写回list集合中
        list_hypothesis_page.append(url)   
    else:
        pass
    finally:
        pass

#验证链接可用性，无法响应的直接干掉
def check_url(parameter_list):
    """
    验证url可用性
    """
    #
    with open('88.html', "r") as fs:
        json_url = fs.read()
        fs.close()

#第一次开始工作时的线程
class first_Thread(threading.Thread):
    def __init__(self, proxies_ip,wd):
        threading.Thread.__init__(self)
        self.proxies_ip = proxies_ip
        self.wd = wd
    def run(self):
        # print("开始线程：" + self.proxies_ip+"\n")
        get_proxies_wd(self.proxies_ip,self.wd)

#根据页码url工作的线程
class url_Thread(threading.Thread):
    def __init__(self, proxies_ip,url):
        threading.Thread.__init__(self)
        self.proxies_ip = proxies_ip
        self.url = url
    def run(self):
        # print("开始线程：" + self.proxies_ip+"\n")
        get_proxies_url(self.proxies_ip,self.url)


#使用了代理，多线程的主方法
def main_proxies_thread():
    global ip_list
    global begin_page_number
    global list_hypothesis_page
    global is_first_bool
    while 1 == 1:
        #是否需要抓取代理IP
        if len(ip_list) == 0:
            time.sleep(1)
            ip_list = parsing_html.get_kuaidaili_free_ip(begin_page_number)
        #开始任务
        while len(ip_list) != 0:
            #获取代理IP
            proxies_ip = ip_list.pop()  # 移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
            #第一次
            if is_first_bool:
                first_Thread(proxies_ip,'free sxe jva').start()
            else:
                print(len(list_hypothesis_page))
                next_url = list_hypothesis_page.pop()
                # 创建新线程
                url_Thread(proxies_ip,next_url).start()
        # #结束线程，当下一页的页码集合为空且第一次抓取成功 时结束任务
        # if len(list_hypothesis_page)==0 and is_first_bool:
        #     print("任务结束！")
        #     break
        begin_page_number += 1

#未使用代理和多线程
def main_reptiles():
    global list_hypothesis_page
    global is_first_bool
    #开始任务
    while len(list_hypothesis_page) > 0 or is_first_bool:
        #第一次
        if is_first_bool:
            get_wd('free sxe jva')
        else:
            next_url = list_hypothesis_page.pop()
            print('url集合剩余数：'+str(len(list_hypothesis_page))+'  '+next_url)
            # 创建新线程
            get_url(next_url)
        #随机休眠3-9秒
        time.sleep(random.randint(3,9))
    

if __name__ == '__main__':
    main_reptiles()
    # main_proxies_thread()
    # # 123.163.115.180:9999
    # get_baidu_wd('free sxe jva', '123.163.115.180:9999','')


# 根据url搜索
def get_baidu_url222(my_url):
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
