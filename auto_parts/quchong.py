#!/usr/bin/python3
 
import pymysql
 
# 打开数据库连接
db = pymysql.connect(host="localhost",
                    port=3306,
                    user="root",
                    passwd="",
                    database="auto_parts")
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

while 1== 1:
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT cellphone FROM `customer_list` where memo = '' LIMIT 1")
    # 使用 fetchone() 方法获取单条数据.
    cellphone1 = cursor.fetchone()
    cursor.execute("SELECT count(*) FROM `costomer_list_new` where cellphone = '%s'"% cellphone1)
    cellphone2 = cursor.fetchone()
    if cellphone2[0] ==0:
        cursor.execute("INSERT INTO `costomer_list_new`(`cellphone`) VALUES ('%s')"%cellphone1)
        cursor.execute("UPDATE `customer_list` SET `memo`='1' WHERE cellphone = '%s'"%cellphone1)
        db.commit()
        print('11')
 
# 关闭数据库连接
db.close()