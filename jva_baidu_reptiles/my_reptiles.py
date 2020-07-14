import requests
from bs4 import BeautifulSoup
import re
import json

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


my_file = open(r".\baidu.html", 'rb')
my_html = my_file.read()
my_soup = BeautifulSoup(my_html, "html.parser")
# for item in my_soup.find_all('div',class_="c-tools"):   #查找符合要求的内容
#     print(item)
#     # print(item.get('data-tools'))
#     # data2 = json.loads(item.get('data-tools'))
#     # print ( data2['title'],data2['url'])

for item in my_soup.find_all('div',class_="page-inner"):
    for item2 in item.find_all('a'):
        print(item2.get_text())
        print('https://www.baidu.com'+item2.get('href'))
