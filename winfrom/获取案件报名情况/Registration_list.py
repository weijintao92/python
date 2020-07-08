
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:wjt
# date:2020-7-8
# descript:获取案件报名情况
 
 
import tkinter as tk  # 使用Tkinter前需要先导入
 
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

#查询结果

 
# 第5步，主窗口循环显示
window.mainloop()