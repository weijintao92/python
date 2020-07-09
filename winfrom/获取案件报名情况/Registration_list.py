
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wjt
# date:2020-7-8
# descript:获取案件报名情况
 
 
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox
import pymssql      #引入sqlserver
 
# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('大数智')
# 第3步，设定窗口的大小(长 * 宽)
# window.geometry('500x300')  # 这里的乘是小x
 
# 画界面
# 案件编号
Label_hs = tk.Label(window, text='案件编号：', font=('Arial', 12))
Label_hs.grid(row=0,column=0)
Entry_hs = tk.Entry(window, show=None, font=('Arial', 14),bd='5')  
Entry_hs.grid(row=0,column=1)
# 案件承办人
Label_cbr = tk.Label(window, text='承办人：', font=('Arial', 12))
Label_cbr.grid(row=0,column=3)
Entry_cbr = tk.Entry(window, show=None, font=('Arial', 14),bd='5')  
Entry_cbr.grid(row=0,column=4)

# 搜索按钮
b = tk.Button(window, text='hit me', font=('Arial', 12))
b.grid(row=1,column=2)

def myPrint(self):
    if(Entry_cbr.get() == '' and  Entry_hs.get()== ""):
        tk.messagebox.showinfo('提示','请输入案件标号或承办人！')
    if(Entry_cbr.get() != '' and  Entry_hs.get()!= ""):
        sql = "select * from tasks where TaskName = '"+Entry_hs.get()+"' or Faguan like '%"+Entry_cbr.get()+"%'"
    if(Entry_cbr.get() == '' and  Entry_hs.get()!= ""):
        sql = "select * from tasks where TaskName = '"+Entry_hs.get()+"'"
    if(Entry_cbr.get() != '' and  Entry_hs.get()== ""):
        sql = "select * from tasks where Faguan like '%"+Entry_cbr.get()+"%'"
    print(sql)
    print(Entry_cbr.get())

b.bind("<Button-1>",myPrint)

# def my_pymssql(my_an,my_cbr):
#     connect = pymssql.connect('2.zhuamm.com', 'sa', 'psy@2020', 'court_juror')  #服务器名,账户,密码,数据库名
#     if connect:
#         print("连接成功!")
        
#     cursor = connect.cursor()   #创建一个游标对象,python里的sql语句都要通过cursor来执行
#     sql = "select * from tasks where TaskName = '"+Entry_hs+"' or Faguan like '%"+Entry_cbr+"%'"
#     print(sql)
#     cursor.execute(sql)   #执行sql语句
#     print(cursor.fetchall())
#     connect.commit()  #提交
#     cursor.close()   
#     connect.close()  




#查询结果

 
# 第5步，主窗口循环显示
window.mainloop()