#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog
# 第1步，实例化object，建立窗口window
window = tk.Tk()
# 第2步，给窗口的可视化起名字
window.title('大数智')
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x
# 窗体加载时运行
# root.withdraw()  

# 调用文件对话框获取文件路径
def my_checkFile():
    file_path = filedialog.askopenfilename()

# 选择数据源
b = tk.Button(window, text='选择json数据源', font=(
    'Arial', 12), command=my_checkFile)
b.pack()

# 开始工作
b_start = tk.Button(window, text='选择json数据源', font=(
    'Arial', 12), command=my_start)
b_start.pack()

# 第5步，主窗口循环显示
window.mainloop()

