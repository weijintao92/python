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
   


def get_baidu_wd(proxies_ip,my_wd):
    # global list_hypothesis_page 
    # global is_first_bool
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

while 1==1:
    # 获取IP列表
    res = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=513ba70ef0acc8958c58bf6bd8f67a3d&random=1&sep=3').content.decode()
    # 按照\n分割获取到的IP
    ips = res.split('\n')
    ips.pop()
    for item in ips:
        get_baidu_wd(item,'free')



