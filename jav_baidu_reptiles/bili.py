'''
author:Ericam
description: 用于爬取b站视频链接
'''
import requests
import re
from lxml import etree
import time
'''
该函数用于解析爬取的网页。
提取出网页里视频的url链接以及对应的视频名。
'''
def getHref(url,page):
try:
req = requests.get(url,timeout=5,headers=headers)
html = req.text
data = etree.HTML(html)
'''
page-1://*[@id="all-list"]/div[1]/div[2]/ul[@class="video-list"]/li
other://*[@id="all-list"]/div[1]/ul[@class="video-list"]/li
'''
pattern = '//*[@id="all-list"]/div[1]/div[2]/ul[contains(@class,"video-list")]/li' if page == 1 else '//*[@id="all-list"]/div[1]/ul[contains(@class,"video-list")]/li'
vurlList = data.xpath(pattern)
for li in vurlList:
vurl = li.xpath(".//a/attribute::href")[0]
title = li.xpath(".//a/attribute::title")[0]
yield vurl,title
except:
print('第%d页爬取失败' % page)
print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
time.sleep(3)
'''
该函数用于正则提取，将url内的BV号提取出来
'''
def getBv(href):
pattern = re.compile('(BV.*?)\?')
data = re.search(pattern,href)
if data == None:
return ''
return data.group(1)
if __name__ == "__main__":
#头部伪装
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
hrefList = []
titleList = []
#需要爬取多少页，自行进行修改，本代码测试1~2页
for i in range(1,3):
url = "https://search.bilibili.com/all?keyword=歪嘴战神&page={0}".format(i) #修改keyword后的关键字即可
l = getHref(url,i)
for vurl,title in l:
hrefList.append(vurl)
titleList.append(title)
print("第{0}页爬取结束".format(i))
time.sleep(2)
print("---------------------------开始截取BV号-----------------------------")
for i in range(len(hrefList)):
hrefList[i] = getBv(hrefList[i])
with open("bv.txt",'w',encoding='utf-8') as f:
for i in range(len(hrefList)):
f.write(hrefList[i]+"\t"+titleList[i]+"\n")
print("爬取结束")