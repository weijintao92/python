#!/usr/bin/python3
# coding=utf-8
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import xlrd
import pymysql

#Date:2020-11
#Author:wjt
#description: mysql 保存电话号码，并剔除重复。

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('将电话导入数据中心，并剔除重复')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x


file_path = ""

# 选择数据源按钮
def my_checkFile():
    global file_path
    file_path = filedialog.askopenfilename()

btn_check = tk.Button(window, text='选择电话号码数据源', font=(
    'Arial', 12), command=my_checkFile)
btn_check.pack()

def my_start():
    if file_path == "":
        return tk.messagebox.showwarning("警告", "请选择数据源！")
    
    try:
        #开始操作数据库
        db = pymysql.connect("db4free.net", "free_auto_parts",
                            "weijintao92", "free_auto_parts")
        if db == False:
            print("连接失败!")
        # 创建一个游标对象,python里的sql语句都要通过cursor来执行
        cursor = db.cursor()
        resuolts = read_xlrd(file_path)
        for target_list in resuolts:
            sql_search = "select count(*) from costomer_list_new where cellphone = '%s'"%(target_list[0],)
            cursor.execute(sql_search)
            if(cursor.fetchall()[0][0] == 0):
                sql_insert ="insert into costomer_list_new values('','%s')"%(target_list[0],)
                cursor.execute(sql_insert)
                db.commit()
                print('加入：'+str(target_list[0]))
            else:
                print('重复：'+str(target_list[0]))
    except:
        tk.messagebox.showwarning("警告", "插入数据时出错了！")
    finally:
        db.close()
# 开始导入数据
b_start = tk.Button(window, text='开始上传', font=(
    'Arial', 12), command=my_start)
b_start.pack()


# 获取excel中的数据
def read_xlrd(excelFile):
    data = xlrd.open_workbook(excelFile)
    table = data.sheet_by_index(0)
    dataFile = []
    for rowNum in range(table.nrows):
        # if 去掉表头
        if rowNum > 0:
            dataFile.append(table.row_values(rowNum))
    return dataFile


if __name__ == '__main__':
    # 主窗口循环显示
    window.mainloop()