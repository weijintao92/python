#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import pymysql


# 打开数据库连接
db = pymysql.connect("db4free.net", "free_auto_parts",
                     "weijintao92", "free_auto_parts")
if db == False:
    print("数据库连接失败!")

# 使用cursor()方法获取操作游标
cursor = db.cursor()
my_db = 'free_auto_parts'
username =123456
# SQL 查询语句
sql = "INSERT into `%s`.`%s` \
SELECT * FROM `%s`.`costomer_list_new` where cellphone not in (select cellphone from `%s`.`%s` )  \
LIMIT 0, %s "%(my_db,username,my_db,my_db,username,100)
print(sql)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    db.commit()
    # print(results)
    # for row in results:
    #     fname = row[0]
    #     lname = row[1]
    #     age = row[2]
    #     sex = row[3]
    #     income = row[4]
    #     # 打印结果
    #     print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" %
    #           (fname, lname, age, sex, income))
except:
    print("程序发生了错误！")
finally:
    # 关闭数据库连接
    db.close()

