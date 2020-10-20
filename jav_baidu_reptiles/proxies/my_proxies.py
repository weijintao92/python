#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2018/7/27
# @Author  : 圈圈烃
# @File    : get_proxy
# @Description: 下载+验证，获取可用ip
#
#
# from checking_ip import *
# from parsing_html import *
import checking_ip
import parsing_html
import time


def main():

    today = time.strftime("%Y_%m_%d")     # 当前日期
    ip_pools_path = "proxies\ip_proxy\\" + today + "_ip_pools.txt"                 # 原始ip保存路径
    ip_format_pools_path = "proxies\ip_proxy\\" + today + "_ip_format_pools.txt"   # 格式化后ip保存路径
    ip_use_path ="proxies\ip_proxy\\" + today + "_ip_use.txt"                     # 可用ip保存路径


    # parsing_html.get_kuaidaili_free_ip(None, ip_pools_path,False)
    checking_ip.ip_format(ip_pools_path,ip_format_pools_path)

if __name__ == '__main__':
    main()
