# !/usr/bin/env/python
# _*_coding:utf-8_*_
# Data:2019-04-07
# Auther:苏莫
# Link:QQ2388873062
# Address:https://blog.csdn.net/lingluofengzang
# PythonVersion:python2.7
# filename:sys_info.py

# import sys
import wmi
import socket
import platform
from multiprocessing import cpu_count
import psutil

# reload(sys)
# sys.setdefaultencoding('utf-8')

c = wmi.WMI()

# 系统信息
print(u'操作系统名称'+platform.platform()[:-(len(platform.version())+1)])
print(u'操作系统版本号'+platform.version())
print(u'操作系统的位数'+platform.architecture()[0])
hostname = socket.getfqdn(socket.gethostname(  ))
ip = socket.gethostbyname(hostname)
print('ip:'+ip)

# CPU信息
def get_CPU():
	cpumsg = []
	for cpu in c.Win32_Processor():
		tmpmsg = {}
		tmpmsg['Name'] = cpu.Name
		tmpmsg['d'] = cpu.Caption 
		tmpmsg['cpu_count'] = cpu_count()
	cpumsg.append(tmpmsg)
	print(cpumsg)

#获取CPU信息

# def GetCpuInfo():
#     cpu_count = psutil.cpu_count(logical=False)  #1代表单核CPU，2代表双核CPU  
#     xc_count = psutil.cpu_count()                #线程数，如双核四线程
#     cpu_slv = round((psutil.cpu_percent(1)), 2)  # cpu使用率
#     list = [cpu_count,xc_count,cpu_slv]
#     print(list)

# # 内存信息
# def get_PhysicalMemory():

# 	memorys = []
# 	for mem in c.Win32_PhysicalMemory():
# 		tmpmsg = {}
# 		tmpmsg['Tag'] = mem.Tag
# 		tmpmsg['ConfiguredClockSpeed'] = str(mem.ConfiguredClockSpeed)+'MHz'
# 		memorys.append(tmpmsg)

# 	print(memorys)

# # 显卡信息
# def get_video():
	
# 	videos = []
# 	for v in c.Win32_VideoController():
# 		tmpmsg = {}
# 		tmpmsg['Caption'] = v.Caption
# 		tmpmsg['AdapterRAM'] = str(abs(v.AdapterRAM)/(1024**3))+'G'
# 		videos.append(tmpmsg)

# 	print videos

# #网卡mac地址
# def get_MacAddress():
	
# 	macs = []
# 	for n in  c.Win32_NetworkAdapter():
# 		mactmp = n.MACAddress
# 		if mactmp and len(mactmp.strip()) > 5:
# 			tmpmsg = {}
# 			tmpmsg['ProductName'] = n.ProductName
# 			tmpmsg['NetConnectionID'] = n.NetConnectionID
# 			tmpmsg['MACAddress'] = n.MACAddress
# 			macs.append(tmpmsg)

# 	print macs

def main():
	# GetCpuInfo()
	get_CPU()
	# get_PhysicalMemory()
	# get_video()
	# get_MacAddress()

if __name__ == '__main__':
	main()
