
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wjt
# date:2020-7-8
# descript:获取案件报名情况

import pymssql

connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020', 'court_juror')  #服务器名,账户,密码,数据库名
if connect:
    print("连接成功!")
    
cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
sql = "select top 1 * from tasks"
cursor.execute(sql)   #执行sql语句
print(cursor.fetchall())
connect.commit()  #提交
cursor.close()   
connect.close()  