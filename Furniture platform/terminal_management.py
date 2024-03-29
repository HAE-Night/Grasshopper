import socket
import tkinter
import subprocess
import os
import time
import re
import sys
import webbrowser
from tkinter import Label, Button, StringVar
from tkinter.messagebox import *

MGR_FILE = "manage.py"
MGR_DIR = 'E:\PythonProject\Furniture_comparison\\'  # Django项目根目录
MGR_PATH = os.path.join(MGR_DIR, MGR_FILE)

root = tkinter.Tk()
setWidth, setHeight = root.maxsize()
root.geometry('320x220+%d+%d' % ((setWidth - 320) / 2, (setHeight) / 2 - 220))
root.title('运行助手')
root.resizable(width=False, height=False)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 这里连接到公共DNS服务器来获取本机对外IP，但可能受到NAT等网络环境影响而并非局域网内的实际IP
        s.connect(('8.8.8.8', 80))  # Google DNS
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'  # 如果出错，则返回回环地址
    finally:
        s.close()
    return local_ip


ip_address = get_local_ip()
print(ip_address)


def open_explo(url):
    print(url)
    webbrowser.open_new_tab("http:" + url)


def find_process():
    proc = subprocess.Popen('netstat -ano | findstr "8000"', shell=True, stdout=subprocess.PIPE).stdout.read()
    return proc


def kill_process(res: str):
    try:
        pid_value = re.findall(r'LISTENING\s+?(\d+)', res.decode())[0]
    except:
        if "TIME_WAIT" in res.decode():
            showwarning(title='提示信息', message='8000 端口未完全释放，请稍候重试。')
        else:
            showwarning(title='提示信息', message='Error: 未知错误')
        root.destroy()
        sys.exit(0)
    subprocess.Popen('taskkill /F /pid %s' % pid_value, shell=True, stdout=subprocess.PIPE)


def check_btn():
    if bvar1.get() == "停止":
        button_index.config(state=tkinter.ACTIVE)
        button_admin.config(state=tkinter.ACTIVE)
    else:
        button_index.config(state=tkinter.DISABLED)
        button_admin.config(state=tkinter.DISABLED)
    root.update()


def state_sw():
    if switch_btn['text'] != "停止":
        run_shell('python manage.py runserver {}'.format(ip_address + ":8000"))
        print("zzzzzz")
        bvar1.set('停止')
        switch_btn['background'] = "#32A084"
        # showinfo(title='提示信息', message='开始运行')
        bottom_message['text'] = "开始运行"
        check_btn()
        time.sleep(0.5)
        bottom_message['text'] = "服务已启动"
    else:
        if askyesno('操作提示', '是否停止服务？', default='no'):
            search_res = find_process()
            if search_res:
                kill_process(search_res)
                bvar1.set('运行')
                bottom_message['text'] = "停止服务"
                check_btn()
                switch_btn['background'] = "#EBEDEF"
                time.sleep(0.5)
                bottom_message['text'] = "就绪"
            else:
                bottom_message['text'] = "未就绪"
                showwarning(title='提示信息', message='服务进程不存在！')
                bvar1.set('运行')
                bottom_message['text'] = "就绪"
                check_btn()
                switch_btn['background'] = "#EBEDEF"


def run_shell(run_param):
    mark = time.strftime('RA+%Y%m%d %H:%M:%S', time.localtime())  # 用于进程名称的特征字符串，方便过滤
    cmd = run_param
    console = subprocess.Popen(cmd, shell=True)
    if run_param == 'python manage.py runserver {}'.format(ip_address + ":8000"):
        return
    root.withdraw()
    console.wait()
    while True:
        task_info = subprocess.Popen('tasklist /V | findstr /C:"%s"' % mark, shell=True, stdout=subprocess.PIPE)
        if not task_info.stdout.read():
            root.deiconify()
            break


bvar1 = StringVar()
bvar1.set('运行')

label1 = Label(root, text='web服务', width=25, borderwidth=2, relief='groove', background='#f60', foreground='white')
switch_btn = Button(root, textvariable=bvar1, background='#EBEDEF', command=state_sw)
label1.grid(row=0, column=0, columnspan=5, padx=15, pady=10, ipadx=5, ipady=6)
switch_btn.grid(row=0, column=5, padx=30, pady=10, ipadx=5, ipady=2)

label2 = Label(root, text='管理终端', width=25, borderwidth=2, relief='groove', background='#f60', foreground='white')
button2 = Button(root, text='运行', background='#EBEDEF', command=lambda: open_explo(ip_address + ":8000/admin"))
label2.grid(row=1, column=0, columnspan=5, padx=15, pady=10, ipadx=5, ipady=6)
button2.grid(row=1, column=5, padx=30, pady=10, ipadx=5, ipady=2)

label3 = Label(root, text='数据库终端', width=25, borderwidth=2, relief='groove', background='#f60', foreground='white')
button3 = Button(root, text='运行', background='#EBEDEF', command=lambda: run_shell('python Visual_Interface.py'))
label3.grid(row=3, column=0, columnspan=5, padx=15, pady=10, ipadx=5, ipady=6)
button3.grid(row=3, column=5, padx=30, pady=10, ipadx=5, ipady=2)

button_index = Button(root, text='首页', command=lambda: open_explo(ip_address + ':8000/'))
button_index.grid(row=4, column=3, padx=10, ipadx=5, ipady=2)
button_admin = Button(root, text='控制台', command=lambda: open_explo(ip_address + ':8000/admin'))
button_admin.grid(row=4, column=4, ipady=2)

bottom_message = Label(foreground='blue', width=36, anchor='w', font=('Arial', 8))
bottom_message.grid(row=5, column=0, columnspan=6, padx=15, ipadx=5, sticky='W')

ifSetup = find_process()
check_btn()
if ifSetup:
    root.withdraw()
    if askyesno(title='提示信息', message='8000 端口已被占用，是否帮您停止对应服务？'):
        kill_process(ifSetup)
        bottom_message['text'] = "就绪"
    else:
        switch_btn.config(state=tkinter.DISABLED)
        bottom_message['text'] = "未就绪"
    root.deiconify()

if __name__ == '__main__':
    root.mainloop()
