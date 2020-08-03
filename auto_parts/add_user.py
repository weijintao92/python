#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pymysql

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('汽配客户管理-后台')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x

# 案件编号
Label_username = tk.Label(window, text='用户名：', font=('Arial', 12))
Label_username.pack()
Entry_username = tk.Entry(window, show=None, font=('Arial', 14), bd='5')
Entry_username.pack()
Label_pwd = tk.Label(window, text='密码：', font=('Arial', 12))
Label_pwd.pack()
Entry_pwd = tk.Entry(window, show=None, font=('Arial', 14), bd='5')
Entry_pwd.pack()
def add_user():
    # 打开数据库连接
    db = pymysql.connect("db4free.net","free_auto_parts","weijintao92","costomer_list_new" )
    if db==False:
        print("数据库连接失败!")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 判断用户是否存在
    sql = "select count(*) from user where user_name = '%s'"%(Entry_username.get(),)
    cursor.execute(sql)
    try:
        # 使用预处理语句创建表
        sql = """CREATE TABLE EMPLOYEE (
        FIRST_NAME  CHAR(20) NOT NULL,
        LAST_NAME  CHAR(20),
        AGE INT,  
        SEX CHAR(1),
        INCOME FLOAT )"""
        cursor.execute(sql)
    except OperationalError:
        tk.messagebox.showwarning("警告", "数据库错误！")
    finally:
        # 关闭数据库连接
        db.close()
    


btn = tk.Button(window, text='增加用户', font=('Arial', 12), command=add_user)
btn.pack()
# 第5步，主窗口循环显示
window.mainloop()


