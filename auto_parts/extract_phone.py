#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pymysql
import datetime

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('电话名单')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x
curr_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
my_db = 'free_auto_parts'
username =123456
def extract_phone():
    # 打开数据库连接
    db = pymysql.connect("db4free.net", "free_auto_parts",
                        "weijintao92", "free_auto_parts")
    if db == False:
        print("数据库连接失败!")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql_a = "INSERT into `%s`.`%s` \
    SELECT *,'%s' FROM `%s`.`costomer_list_new` where cellphone not in (select cellphone from `%s`.`%s` )  \
    LIMIT 0, %s "%(my_db,username,time_str,my_db,my_db,username,100)
    sql_b = "select * from `%s` where time = '%s'"%(username,time_str)
    try:
        # 存储提取记录
        cursor.execute(sql_a)
        db.commit()
        #获取提取记录
        cursor.execute(sql_b)
        results = cursor.fetchall()
        # print(results)

        with open(time_str.replace(' ','-').replace(':','-')+'.vcf', 'w') as v:
        # with open('abc.vcf', 'w') as v:
            for row in results:
                v.write("BEGIN:VCARD"+"\n")
                v.write("VERSION:2.1"+"\n")
                v.write("N:;"+str(row[0])+";;;\n")
                v.write("TEL;CELL:"+str(row[1])+"\n")
                v.write("END:VCARD"+"\n")
    except:
        print("程序发生了错误！")
    finally:
        # 关闭数据库连接
        db.close()


btn = tk.Button(window, text='获取用户名单', font=('Arial', 12), command=extract_phone)
btn.pack()
# 第5步，主窗口循环显示
window.mainloop()

