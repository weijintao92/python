#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
# import pymysql
import datetime
import sqlite3

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('客户名单管理2020-11-11')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('300x300')  # 这里的乘是小x
curr_time = datetime.datetime.now()
time_str = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
my_db = 'free_auto_parts'
table_user =123456

def extract_phone():
    """
        mysql
    """
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
    LIMIT 0, %s "%(my_db,table_user,time_str,my_db,my_db,table_user,100)
    sql_b = "select * from `%s` where time = '%s'"%(table_user,time_str)
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

def extract_phone_sqlite3():
    """
        sqlite3
    """
    count  = E2.get()
    #  isdigit() 方法检测字符串是否只由数字组成。
    if count.isdigit() is False:
        tk.messagebox.showwarning("警告！", "提取数量只能为数字且不能为空！")
        E2.focus()
        return

    my_db = 'main'
    table_user =123456
    # 打开数据库连接
    conn = sqlite3.connect('customer.db')
    if conn == False:
        print("数据库连接失败!")
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # 组装sql语句
    sql_insert = "INSERT into `%s`.`%s` \
    SELECT *,'%s' FROM `%s`.`costomer_list` where cellphone not in (select cellphone from `%s`.`%s` )  \
    LIMIT 0, %s "%(my_db,table_user,time_str,my_db,my_db,table_user,int(count))
    sql_select = "select * from `%s` where time = '%s'"%(table_user,time_str)
    try:
        # 存储提取记录
        cursor.execute(sql_insert)
        conn.commit()
        #获取提取记录
        cursor.execute(sql_select)
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
        tk.messagebox.showinfo("成功", "提取电话号码成功！文件名称为："+time_str.replace(' ','-').replace(':','-')+'.vcf')
        # tk.messagebox.OK()
    except:
        conn.rollback() #回滚
        print("提取数据时发生了错误！")
        tk.messagebox.showerror("错误", "提取数据时发生了错误！")
    finally:
        # 关闭数据库连接
        conn.close()

def add_cellphone():
    """
    往数据中心，新增电话
    """

    phonenumber  = E1.get()
    #  isdigit() 方法检测字符串是否只由数字组成。
    if phonenumber.isdigit() is False:
        tk.messagebox.showwarning("警告！", "电话号码只能为数字且不能为空！")
        E2.focus()
        return
    try:
        # 打开数据库连接
        conn = sqlite3.connect('customer.db')
        if conn == False:
            print("数据库连接失败!")
        # 使用cursor()方法获取操作游标
        cursor = conn.cursor()

        sql_search = "select * from costomer_list where cellphone = '%s'"%(phonenumber,)
        cursor.execute(sql_search)
        list_results =cursor.fetchall()
        if len(list_results) ==0:   
            sql_insert ="insert into costomer_list(cellphone) values('%s')"%(phonenumber,)
            cursor.execute(sql_insert)
            conn.commit()
            tk.messagebox.showinfo("成功", "新增成功！") 
        else:
            tk.messagebox.showwarning("提示", "数据中心已存在此电话！"+str(phonenumber))  
    except Exception:
        conn.rollback()
        print("新增数据时发生了错误！")
        tk.messagebox.showerror("错误", "新增数据时发生了错误！")
    finally:
        conn.close()

#columnspan和rowspan参数的使用

#新增客户名单
L1 = tk.Label(text="电话号码：")
L1.grid(row=0,column=0)
E1 = tk.Entry(bd =5)
E1.grid(row = 0 ,column = 1)

btn_add = tk.Button(window, text='提交', font=('Arial', 12), command=add_cellphone)
btn_add.grid(row =0 ,column = 2 )


#提取电话号码
L2 = tk.Label(text="提取数量：")
L2.grid(row=2,column=0)
E2 = tk.Entry(bd =5)
E2.insert(0,"50")
E2.grid(row = 2 ,column = 1)

btn = tk.Button(window, text='提取', font=('Arial', 12), command=extract_phone_sqlite3)
btn.grid(row =2 ,column =2)



# 第5步，主窗口循环显示
window.mainloop()

