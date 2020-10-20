#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/27
# @Author  : 圈圈烃
# @File    : parsing_html
# @Description: 解析ip代理网站中免费的ip位置并提取, 目前有以下网站：
# 1. 无忧代理  : http://www.data5u.com/
# 2. 快代理   : https://www.kuaidaili.com/
# 3. 小舒代理  : http://www.xsdaili.com/
# 4. 西刺代理  : http://www.xicidaili.com/
# 5. 89免费代理: http://www.89ip.cn/
#
#
from bs4 import BeautifulSoup
import requests
import re

def get_html(url, open_proxy=False, ip_proxies=None):
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
        if open_proxy:   # 判断是否开启代理
            proxies = {"http": "http://" + ip_proxies, }  # 设置代理，例如{"http": "http://103.109.58.242:8080", }
            res = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        else:
            res = requests.get(url, headers=headers, timeout=5)
        # res.encoding = res.apparent_encoding  # 自动确定html编码,由于这里可能导致乱码，先注释掉
        print("Html页面获取成功 " + url)
        return res.text     # 只返回页面的源码
    except Exception as e:
        print("Html页面获取失败 " + url)
        print(e)


def save_ip(data, save_path):
    """
    将获取的ip信息保存到文件中
    :param data: 代理ip数据，数据类型为列表
    :param save_path: 代理ip保存路径
    :return:
    """
    try:
        print("总共获取 " + str(len(data)) + " 条数据")
        with open(save_path, "a") as f:
            for i in range(len(data)):
                f.write(data[i])
            f.close()
            print("文件保存成功")
    except Exception as e:
        print("文件保存失败！！！")
        print(e)


def get_kuaidaili_free_ip(ip_proxies, save_path, open_proxy):
    """
    获取快代理的免费ip
    :param ip_proxies: 要使用的代理ip（这里是用代理ip去爬代理ip）
    :param save_path: 代理ip保存路径
    :param open_proxy: 是否开启代理，默认为False
    :return:
    """
    ip_list_sum = []    # 代理ip列表
    for i in range(10):  # 获取页数
        res_text = get_html("https://www.kuaidaili.com/ops/proxylist/" + str(i+1) + "/", open_proxy=open_proxy,
                            ip_proxies=ip_proxies)
        # 页面解析
        soup = BeautifulSoup(res_text, "html.parser")
        tags = soup.find_all("div", id="freelist")
        for tag in tags:
            ip_list = []
            sps = tag.find_all("td")
            for sp in sps:
                my_text = sp.get_text()
                if  my_text.isdigit() or my_text.find('.') != -1 :
                    ip_info = sp.get_text()
                    ip_list.append(ip_info)         
            for j in range(10):      # 每页100条数据
                ip_info_format = ""
                for k in range(8):   # 每条6个内容
                    if k == 7:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "\n"
                    else:
                        ip_info_format += str(ip_list[(j * 8 + k)]) + "___"
                ip_list_sum.append(ip_info_format)
    save_ip(ip_list_sum, save_path)

    

if __name__ == "__main__":
    print(1)
    get_kuaidaili_free_ip('','D:\github\python\jav_baidu_reptiles\ss.txt',False)




