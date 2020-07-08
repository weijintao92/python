import tkinter

win = tkinter.Tk()
win.title("Listbox列表框")
win.geometry("800x600+600+100")

lbv=tkinter.StringVar()#绑定变量
#SINGLE与BORWSE作用相似，但是不支持鼠标按下后移动选中位置
lb=tkinter.Listbox(win,selectmode=tkinter.SINGLE,listvariable=lbv)
lb.pack()
for item in["good","nice","handsome","very good","verynice"]:

    lb.insert(tkinter.END,item)

lb.insert(tkinter.ACTIVE,"cool")
#打印当前列表的选项
print(lbv.get())
#设置选项,把列表值变为1，2，3
#lbv.set(("1","2","3"))
#绑定事件
def myPrint(self):
    print(lb.curselection())#提取点中选项的下标
    print(lb.get(lb.curselection()))#提前点中选项下标的值
lb.bind("<Double-Button-1>",myPrint)
#"<Double-Button-1>"  鼠标双击
win.mainloop()