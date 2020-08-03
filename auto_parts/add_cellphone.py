#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 外地法院
from tkinter import ttk
import json
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import time
import pymysql
# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('增加电话并去除重复的')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x
# 窗体加载时运行
# root.withdraw()
file_path = ""


# 调用文件对话框获取文件路径
def my_checkFile():
    global file_path
    file_path = filedialog.askopenfilename()


# 选择数据源
b = tk.Button(window, text='选择电话数据源', font=(
    'Arial', 12), command=my_checkFile)
b.pack()


def my_start():
    if file_path == "":
        return tk.messagebox.showwarning("警告", "请选择json数据源")

    db = pymysql.connect("db4free.net", "free_auto_parts",
                        "weijintao92", "free_auto_parts")
    if con == False:
        print("连接失败!")
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor = db.cursor()
    try:
        # 读取json文件内容,返回字典格式，并加入my_transfer库中
        with open(file_path, 'r', encoding="utf-8")as fp:

            cursor.execute(my_sql)  # 执行sql语句
        cursor.execute("select count(*) from transfer.dbo.g_ajz")
        print('g_ajz原始数据行数：'+str(cursor.fetchall()))
        # 执行数据筛选的存储过程
        cursor.execute(f"exec transfer.dbo.insert_my_anjian_tb")
        db.commit()
        cursor.execute("select count(*) from transfer.dbo.g_ajz")
        print('g_ajz当前数据行数：'+str(cursor.fetchall()))
        tk.messagebox.showwarning("提示", "完成！")
    except UnicodeDecodeError:
        tk.messagebox.showwarning("警告", "文本编码格式需为utf-8")
    finally:
        # 关闭数据库链接
        db.close()


# 开始工作
b_start = tk.Button(window, text='开始上传', font=(
    'Arial', 12), command=my_start)
b_start.pack()

# 第5步，主窗口循环显示
window.mainloop()
