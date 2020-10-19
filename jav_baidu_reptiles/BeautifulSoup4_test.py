# beautifulsoup4_test.py
 
from bs4 import BeautifulSoup
 
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
 
#创建 Beautiful Soup 对象
soup = BeautifulSoup(html)
 
#打开本地 HTML 文件的方式来创建对象
#soup = BeautifulSoup(open('index.html'))
 
# print(soup.name)
# [document] #soup 对象本身比较特殊，它的 name 即为 [document]
 
# print(soup.head.name)
# # head #对于其他内部标签，输出的值便为标签本身的名称
 
# print(soup.p.attrs)
# # {'class': ['title'], 'name': 'dromouse'}
# # 在这里，我们把 p 标签的所有属性打印输出了出来，得到的类型是一个字典。
 
print(soup.p['class']) # soup.p.get('class')
# # ['title'] #还可以利用get方法，传入属性的名称，二者是等价的
 
# soup.p['class'] = "newClass"
# print(soup.p) # 可以对这些属性和内容等等进行修改
# # <p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
 
# del soup.p['class'] # 还可以对这个属性进行删除
# print(soup.p)
# # <p name="dromouse"><b>The Dormouse's story</b></p>