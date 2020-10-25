#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 20120/10/24
# @Author  : wjt
# @File    : parsing_html
# @Description: 获取快代理IP 集合

from bs4 import BeautifulSoup
import requests
import re
import time


def get_html(url):
    """
    获取页面的html文件
    :param url: 待获取页面的链接
    :param open_proxy: 是否开启代理，默认为False
    :param ip_proxies: 若开启，代理地址
    :return:
    """
    try:
        pattern = re.compile(r'//(.*?)/')
        host_url = pattern.findall(url)[0]
        headers = {
            "Host": host_url,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }
        res = requests.get(url, headers=headers, timeout=5)
        # res.encoding = res.apparent_encoding  # 自动确定html编码,由于这里可能导致乱码，先注释掉
        print("抓取代理IP Html页面获取成功 " + url)
        return res.text     # 只返回页面的源码
    except Exception as e:
        print("抓取代理IP Html页面获取失败 " + url)
        print(e)

def get_kuaidaili_free_ip(begin_page_number):
    """
    获取快代理的免费ip,一次只获取100个
    :param ip_proxies: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 代理ip保存路径
    :param open_proxy: 是否开启代理，默认为False
    :return:
    """
    ip_list_sum = []    # 代理ip列表
    a = 1
    while a<=1:  # 获取页数
        #开始爬取
        r = get_html("https://www.kuaidaili.com/free/inha/" + str(begin_page_number+a) + "/")
        # print("-10"+"\\"+"n")
        if(r == "-10\n"):
            return print("爬取代理IP操作太频繁！")
        # 页面解析
        soup = BeautifulSoup(r, "html.parser")
        tags_ip = soup.tbody.find_all(attrs={"data-title": "IP"} )
        tags_port = soup.tbody.find_all(attrs={"data-title": "PORT"} )
        min_index =0
        max_index = len(tags_ip)-1
        while min_index<=max_index:
            ip_info = tags_ip[min_index].get_text()+":"+tags_port[min_index].get_text()
            ip_list_sum.append(ip_info)
            min_index+=1
        a+=1
    return ip_list_sum
    
if __name__ == "__main__":
   get_kuaidaili_free_ip(1)
    






