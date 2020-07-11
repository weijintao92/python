
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wjt
# date:2020-7-8
# descript:获取案件报名情况


import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pymssql  # 引入sqlserver
import calendar
import datetime
from datetime import timedelta

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('大数智')
# 第3步，设定窗口的大小(长 * 宽)
# window.geometry('500x300')  # 这里的乘是小x

# 画界面
# 案件编号
Label_hs = tk.Label(window, text='案件编号：', font=('Arial', 12))
Label_hs.pack()
Entry_hs = tk.Entry(window, show=None, font=('Arial', 14), bd='5')
Entry_hs.pack()
# 案件承办人
Label_cbr = tk.Label(window, text='承办人：', font=('Arial', 12))
Label_cbr.pack()
Entry_cbr = tk.Entry(window, show=None, font=('Arial', 14), bd='5')
Entry_cbr.pack()

# 搜索


def my_search():
    # 删除listbox和text里的内容
    lb.delete(0, lb.size())
    if(Entry_cbr.get() == '' and Entry_hs.get() == ""):
        tk.messagebox.showinfo('提示', '请输入案件标号或承办人！')
    if(Entry_cbr.get() != '' and Entry_hs.get() != ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.TaskName = '" + \
            Entry_hs.get()+"' and a.Faguan like '%"+Entry_cbr.get()+"%'"
    if(Entry_cbr.get() == '' and Entry_hs.get() != ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.TaskName = '"+Entry_hs.get()+"'"
    if(Entry_cbr.get() != '' and Entry_hs.get() == ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.Faguan like '%"+Entry_cbr.get()+"%'"
    print(my_sql)
    # 创建数据库链接
    connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020',
                              'court_juror', charset='utf8')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(my_sql)  # 执行sql语句
    # print(cursor.fetchall())

    for item in iter(cursor.fetchall()):
        lb.insert(item[0], item[1].encode('latin1').decode('gbk')+','+str(item[0]))
        # print(item[1].encode('latin1').decode('gbk'))
    # 关闭链接
    cursor.close()
    connect.close()


# 搜索按钮
b = tk.Button(window, text='搜索', font=('Arial', 12), command=my_search)
b.pack()


def myPrint(self):
    # print(lb.curselection()) 
    my_text.delete("1.0",tk.END)
    # my_text.delete(0, 'end')
    connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020','court_juror', charset='utf8') 
    if connect:
        print("连接成功!")
    cursor = connect.cursor() 
    my_id = lb.get(lb.curselection()).split(",")[1]
    print(my_id)
    now = datetime.datetime.now()
    print(datetime.datetime(now.year, 1, 1))
    sql_2 = "select c.Name,Cell,COUNT(*) from Task_SMS_Rcv as a left join tasks as b on b.memo like '%'+ a.cell+'%' left join juror_info as c on a.Cell = c.CellPhone where a.extraID = '" + \
        str(my_id)+"' and b.StartDate>'"+ str(datetime.datetime(now.year, 1, 1))+"' group by a.Cell,c.name order by COUNT(*)"
    print(sql_2)
    cursor.execute(sql_2) 
    # print(cursor.fetchall())
    for item in iter(cursor.fetchall()):
        my_text.insert("insert",item[0]+str(item[1])+"本年度陪审次数："+str(item[2]))
        my_text.insert(tk.INSERT, '\n')
        # print(item[1].encode('latin1').decode('gbk'),'\n')

    cursor.close()
    connect.close()


# 列表
lb = tk.Listbox(window, selectmode=tk.SINGLE, width=50)
lb.pack()
lb.bind("<Double-Button-1>", myPrint)



# 输出内容
# 创建滚动条
scroll = tkinter.Scrollbar()
# 创建文本框text，设置宽度100，high不是高度，是文本显示的行数设置为3行
my_text = tkinter.Text(window, width=50)
# 将滚动条填充
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
my_text.pack(side=tkinter.LEFT,fill=tkinter.Y) # 将文本框填充进wuya窗口的左侧，
# 将滚动条与文本框关联
scroll.config(command=my_text.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
my_text.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框
my_text.pack()


# 第5步，主窗口循环显示
window.mainloop()
