#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import datetime

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

#传入搜索关机字
def get_baidu_wd(my_wd):
    # 构建查询条件
    my_params = {'wd': my_wd}
    # 定制请求头
    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
        'Accept': '*/*'
    }
    resoult = requests.get('https://www.baidu.com/s?ie=UTF-8',
                    params=my_params, headers=my_headers)
    return resoult.text

#传入url
def get_baidu_url(my_url):
    # 定制请求头
    my_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
        'Accept': '*/*'
    }
    resoult = requests.get(my_url, headers=my_headers)
    return resoult.text



# my_file = open(r".\baidu.html", 'rb')
# my_html = my_file.read()
# my_soup = BeautifulSoup(my_html, "html.parser")
# for item in my_soup.find_all('div',class_="c-tools"):   #查找符合要求的内容
#     print(item)
#     # print(item.get('data-tools'))
#     # data2 = json.loads(item.get('data-tools'))
#     # print ( data2['title'],data2['url'])
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
        print(datetime.datetime.now())
        time.sleep(0.1)
    # else:
    #     # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
    #     list_pop = list_temp.pop()
    #     list_data = list_data+list_temp
    #     my_bool = 'false'

for target_list in list_data:
    print(target_list['number'])
    

# if __name__ == "__main__":





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
