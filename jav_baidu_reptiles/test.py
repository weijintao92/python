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



with open('sss.html', "rb") as fs:
    my_html = fs.read()
    fs.close()
soup = BeautifulSoup(my_html, "html.parser")
tags_page = soup.find_all(attrs={"srcid": "1599"} )
list_page = []
list_name =[]
# list_descript =[]
for item in tags_page:
    # print(item)
    #获取名称
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
print(list_page)