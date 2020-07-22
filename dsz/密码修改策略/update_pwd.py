import getpass
import subprocess
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog
from my_function import my_function

# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('大数智')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x
# 窗体加载时运行
# root.withdraw()
path_api = ""
path_web = ""

# 选择文件的方法


def checkFile_api():
    global path_api
    path_api = tk.filedialog.askopenfilename()


def checkfile_web():
    global path_web
    path_web = tk.filedialog.askopenfilename()


def my_strat():
    my_function.func_1()


# 选择数据源
btn_api = tk.Button(window, text='选择API配置文件', font=(
    'Arial', 12), command=checkFile_api)
btn_api.pack()
# 选择数据源
btn_web = tk.Button(window, text='选择WEB配置文件', font=(
    'Arial', 12), command=checkfile_web)
btn_web.pack()

# 选择数据源
btn_start = tk.Button(window, text='开始', font=(
    'Arial', 12), command=my_strat)
btn_start.pack()


# 第5步，主窗口循环
window.mainloop()


