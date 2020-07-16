#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import time
import pymssql
# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('大数智')
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
b = tk.Button(window, text='选择json数据源', font=(
    'Arial', 12), command=my_checkFile)
b.pack()


def my_start():
    # 创建数据库链接
    con = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020',
                            'court_juror', charset='utf8')  # 服务器名,账户,密码,数据库名
    if con:
        print("连接成功!")
    cursor = con.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    try:
        
        # 读取json文件内容,返回字典格式
        with open(file_path, 'r', encoding="utf-8")as fp:
            json_data = json.load(fp)
            # print(json_data)
            for item in json_data:
                #案号
                hs = item['AH'].replace(item['AH'][0:11],'').replace(item['DZ'],'').replace('号','')
                fyjc = item['AH'][6:11]
                nh = item['AH'][1:5]
                updatedt = item['LARQ'][0:4]+'-'+item['LARQ'][4:6]+'-'+item['LARQ'][6:8]
                my_sql = "insert into my_transfer.dbo.g_dsz(nh,hs,ay,ay_detail,fyjc,cbr,dsr,memo,clientinfo,updatedt) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
                    %(nh,hs,item['DZ'],item['AYMS'],fyjc,item['YHXM'],item['DSR'],item['DZ'],item['AJMC'],updatedt)

                cursor.execute(my_sql)  # 执行sql语句
                print(cursor.rowcount, "记录插入成功。")
        con.commit()
    except UnicodeDecodeError:
        tk.messagebox.showwarning("警告", "文本编码格式需为utf-8")
    finally:
        # 关闭链接
        cursor.close()
        con.close()

# 开始工作
b_start = tk.Button(window, text='开始工作', font=(
    'Arial', 12), command=my_start)
b_start.pack()

# 第5步，主窗口循环显示
window.mainloop()
