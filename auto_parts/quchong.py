#!/usr/bin/python3
 
import pymysql
 
# 打开数据库连接
db = pymysql.connect(host="192.168.149.18",
                    port=3307,
                    user="root",
                    passwd="123456",
                    database="customer")
 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

while 1== 1:
    # 使用 execute()  方法执行 SQL 查询 
    cursor.execute("SELECT cellphone FROM `transitWarehouse` where memo = 0 LIMIT 1")
    # 使用 fetchone() 方法获取单条数据.
    cellphone1 = cursor.fetchone()
    cursor.execute("SELECT count(*) FROM `ListManagementAPI_customerlist` where cellphone = '%s'"% cellphone1)
    cellphone2 = cursor.fetchone()
    if cellphone2[0] ==0:
        cursor.execute("INSERT INTO `ListManagementAPI_customerlist`(`cellphone`) VALUES ('%s')"%cellphone1)
        cursor.execute("UPDATE `transitWarehouse` SET `memo`='1' WHERE cellphone = '%s'"%cellphone1)
        db.commit()
        print(cellphone1)
 
# 关闭数据库连接
db.close()