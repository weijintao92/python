import getpass
import subprocess

try:
    # 获取计算机用户名
    user = getpass.getuser()
    my_resole =  subprocess.Popen(['net', 'User', user, 'weijintao92'])  # 在本地执行（类似于cmd命令）
    print(my_resole)
except expression as identifier:
    print('失败！')