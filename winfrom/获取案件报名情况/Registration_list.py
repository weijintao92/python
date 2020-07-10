
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wjt
# date:2020-7-8
# descript:获取案件报名情况


import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pymssql  # 引入sqlserver

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

# 列表
lb = tk.Listbox(window, selectmode=tk.SINGLE, width=50)
lb.pack()
# 搜索


def my_search():
    if(Entry_cbr.get() == '' and Entry_hs.get() == ""):
        tk.messagebox.showinfo('提示', '请输入案件标号或承办人！')
    if(Entry_cbr.get() != '' and Entry_hs.get() != ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.TaskName = '" + \
            Entry_hs.get()+"' or a.Faguan like '%"+Entry_cbr.get()+"%'"
    if(Entry_cbr.get() == '' and Entry_hs.get() != ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.TaskName = '"+Entry_hs.get()+"'"
    if(Entry_cbr.get() != '' and Entry_hs.get() == ""):
        my_sql = "select a.id,CAST(b.nh as varchar)+CAST(b.fyjc as varchar)+CAST(b.az as varchar)+CAST(b.hs as varchar)+CAST(b.dsr as varchar) as my_ah from tasks as a left join transfer.dbo.g_ajz as b on a.anjian_id = b.number where a.Faguan like '%"+Entry_cbr.get()+"%'"
    print(my_sql)
    # 创建数据库链接
    connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020',
                              'court_juror', charset='cp936')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(my_sql.encode('cp936'))  # 执行sql语句
    # print(cursor.fetchall())
    # 删除所有元素
    # if lb.size() > 0 :
    lb.delete(0, lb.size())
    for item in iter(cursor.fetchall()):
        lb.insert(item[0], str(item[0])+','+str(item[1]))
        # print(str(item[0])+str(item[1]))
    # 关闭链接
    cursor.close()
    connect.close()


# 搜索按钮
b = tk.Button(window, text='搜索', font=('Arial', 12), command=my_search)
b.pack()


def myPrint(self):
    print(lb.curselection())  # 提取点中选项的下标
    # 创建数据库链接
    connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020','court_juror', charset='cp936')  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    my_id = lb.get(lb.curselection()).split(",")[0]
    print(lb.get(lb.curselection()).split(","))
    sql = "select Row_Number() over ( order by getdate() ) as init , '电话：'+cast(a.Cell as varchar)+'    次数：'+ cast(COUNT(*) as varchar) from Task_SMS_Rcv as a left join tasks as b on b.memo like '%'+ a.cell+'%' where a.extraID = '" + \
        str(my_id)+"' group by a.Cell"
    print(sql)
    cursor.execute(sql.encode('cp936'))  # 执行sql语句
    print(cursor.fetchall())
    # for item in iter(cursor.fetchall()):
    #     lb_text.insert(item[0],item[1])
    
    # 关闭链接
    cursor.close()
    connect.close()


lb.bind("<Double-Button-1>", myPrint)

# 输出内容
lb_text = tk.Listbox(window, selectmode=tk.SINGLE, width=50)
lb_text.pack()


# 第5步，主窗口循环显示
window.mainloop()
